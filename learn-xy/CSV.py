import csv
import gc
import glob
import os
import shutil

import numpy as np

import Config as conf


def getFloatRawCSV(filePath):
    return [[float(cell) for cell in line]
            for line in csv.reader(open(filePath, "r"))]


def getIntRawCSV(filePath):
    return [[int(cell) for cell in line]
            for line in csv.reader(open(filePath, "r"))]


def mergeCSV():
    # Check output directory
    mergedDir = conf.MERGED_DIR.format(conf.WINDOW_SIZE, conf.N_COLUMNS,
                                       conf.THRESHOLD)
    if os.path.exists(mergedDir):
        print("Old files found. Remove them to continue...")
        shutil.rmtree(mergedDir)
        while os.path.exists(mergedDir):
            pass
    os.makedirs(mergedDir)

    # Calculate and save
    xx = np.empty([0, conf.WINDOW_SIZE, conf.N_COLUMNS], float)
    yy = np.empty([0, conf.N_CLASSES], float)
    iSave = 0
    jSave = 0
    for src in conf.SOURCES:
        print("Create window of " + src + " ...")

        # Specify paths
        srcCSIs = sorted(glob.glob(conf.SOURCE_PATH.format("csi", src)))
        srcActions = sorted(glob.glob(conf.SOURCE_PATH.format("action", src)))

        # Calculate merges of X
        i = 0
        rawCSV = np.empty([0, 1 + conf.PKT_COLUMNS * 2], float)
        while i < len(srcCSIs):
            print("Processing X: ", srcCSIs[i])

            # Read CSV
            rawCSV = np.concatenate(
                (rawCSV, np.array(getFloatRawCSV(srcCSIs[i]))), axis=0)

            while True:
                if len(rawCSV) < conf.WINDOW_SIZE:
                    i += 1
                    break
                else:
                    window = np.dstack(
                        rawCSV[0:conf.WINDOW_SIZE,
                               conf.COL_START:conf.COL_START + conf.N_COLUMNS].T
                    )
                    xx = np.concatenate((xx, window), axis=0)
                    rawCSV = rawCSV[conf.SLIDE_SIZE:, :]

            while len(xx) > (iSave + 1) * 200:
                mergedCSIPath = conf.MERGED_PATH.format(
                    conf.WINDOW_SIZE, conf.N_COLUMNS, conf.THRESHOLD, "csi", str(iSave + 1).zfill(3))
                print("Saving X of 200 windows:", mergedCSIPath)
                with open(mergedCSIPath, "w") as out:
                    csv.writer(out, lineterminator="\n").writerows(
                        xx[iSave * 200:(iSave + 1) * 200].reshape(200, -1))
                iSave += 1

        # Calculate merges of Y
        j = 0
        rawCSV = np.empty([0, 2], float)
        while j < len(srcActions):
            print("Processing Y: ", srcActions[j])

            # Read CSV
            rawCSV = np.concatenate(
                (rawCSV, np.array(getFloatRawCSV(srcActions[j]))), axis=0)

            while True:
                if len(rawCSV) < conf.WINDOW_SIZE:
                    j += 1
                    break
                else:
                    window = rawCSV[0:conf.WINDOW_SIZE, 1]
                    yCount = np.zeros(conf.N_CLASSES)
                    for k in range(conf.WINDOW_SIZE):
                        yCount[int(window[k])] += 1
                    for k in range(conf.N_CLASSES):
                        if yCount[k] >= conf.THRESHOLD_PKT:
                            yCount[k] = 1
                        else:
                            yCount[k] = 0
                    if np.sum(yCount) == 0:
                        yCount[0] = 1
                    yy = np.concatenate((yy, yCount[np.newaxis, ...]), axis=0)
                    rawCSV = rawCSV[conf.SLIDE_SIZE:, :]

            while len(yy) > (jSave + 1) * 200:
                mergedActionPath = conf.MERGED_PATH.format(
                    conf.WINDOW_SIZE, conf.N_COLUMNS, conf.THRESHOLD, "action", str(jSave + 1).zfill(3))
                print("Saving Y of 200 windows:", mergedActionPath)
                with open(mergedActionPath, "w") as out:
                    csv.writer(out, lineterminator="\n").writerows(
                        yy[jSave * 200:(jSave + 1) * 200])
                jSave += 1

        gc.collect()

    # Save other all
    print("Saving remained windows")
    if len(xx) % 200 > 0:
        mergedCSIPath = conf.MERGED_PATH.format(
            conf.WINDOW_SIZE, conf.N_COLUMNS, conf.THRESHOLD, "csi", str(iSave + 1).zfill(3))
        print("Saving X of", len(xx[iSave * 200:]), "windows:", mergedCSIPath)
        with open(mergedCSIPath, "w") as out:
            csv.writer(out, lineterminator="\n").writerows(
                xx[iSave * 200:].reshape(len(xx[iSave * 200:]), -1))
    if len(yy) % 200 > 0:
        mergedActionPath = conf.MERGED_PATH.format(
            conf.WINDOW_SIZE, conf.N_COLUMNS, conf.THRESHOLD, "action", str(jSave + 1).zfill(3))
        print("Saving Y of", len(yy[jSave * 200:]), "windows:", mergedActionPath)
        with open(mergedActionPath, "w") as out:
            csv.writer(out, lineterminator="\n").writerows(
                yy[jSave * 200:])

    # Print the results
    print("Shape notice: [xx]", xx.shape, "[yy]", yy.shape)

    return xx, yy


def getCSV():
    # Check whether if input directory exists
    if not os.path.exists(
            conf.MERGED_DIR.format(conf.WINDOW_SIZE, conf.N_COLUMNS,
                                   conf.THRESHOLD)):
        print("-- Input directory not found. Calculate merged CSVs...")
        xx, yy = mergeCSV()
        print("Calculation finished!")
        print("CSV data automatically imported from cache.")

        if not conf.USE_NOACTIVITY:
            print(" -- Eliminating No-Activity windows")
            rows, cols = np.where(yy > 0)
            xx = np.delete(xx,
                           rows[np.where(cols == 0)], 0)
            yy = np.delete(yy,
                           rows[np.where(cols == 0)], 0)
            print(" -- Finished")
        else:
            print(" -- Using No-Activity window.")

        print("Converted and Loaded CSVs.")
        gc.collect()

        return xx, yy

    else:
        print("Importing CSV files...")

        # Specify paths
        mgCSIs = sorted(glob.glob(conf.MERGED_PATH.format(
            conf.WINDOW_SIZE, conf.N_COLUMNS, conf.THRESHOLD, 'csi', '*')))
        mgActions = sorted(glob.glob(conf.MERGED_PATH.format(
            conf.WINDOW_SIZE, conf.N_COLUMNS, conf.THRESHOLD, 'action', '*')))

        xx = None
        yy = None

        # Load CSVs
        for mg in mgCSIs:
            print(" -- Loading:", mg)
            if xx is None:
                xx = np.array(getFloatRawCSV(mg))
            else:
                xx = np.concatenate((xx, np.array(getFloatRawCSV(mg))))
        for mg in mgActions:
            print(" -- Loading:", mg)
            if yy is None:
                yy = np.array(getFloatRawCSV(mg))
            else:
                yy = np.concatenate((yy, np.array(getFloatRawCSV(mg))))

        # Reshape them
        print(" -- Reshaping xx ...")
        xx = xx.reshape(len(xx), conf.WINDOW_SIZE, conf.N_COLUMNS)
        print(" -- Shape notice: [xx]", xx.shape, "[yy]", yy.shape)

        if not conf.USE_NOACTIVITY:
            print(" -- Eliminating No-Activity windows")
            rows, cols = np.where(yy > 0)
            xx = np.delete(xx,
                           rows[np.where(cols == 0)], 0)
            yy = np.delete(yy,
                           rows[np.where(cols == 0)], 0)
            print(" -- Finished")
        else:
            print(" -- Using No-Activity window.")

        print("Loaded CSVs")
        gc.collect()

        return xx, yy


if __name__ == "__main__":
    mergeCSV()
