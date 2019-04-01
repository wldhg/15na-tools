import csv
import glob
import os
import shutil

import numpy as np
import pandas as pd

import Config as conf


def mergeCSVOfAction(xPath, yPath):

    xx = np.empty([0, conf.WINDOW_SIZE, conf.PKT_COLUMNS], float)
    yy = np.empty([0, conf.N_CLASSES], float)

    # Process X
    xCSVPaths = sorted(glob.glob(xPath))
    for csvFile in xCSVPaths:
        print("Processing X: ", csvFile)

        # Read CSV and prepare temporary variables
        rawCSV = [[float(cell) for cell in line]
                  for line in csv.reader(open(csvFile, "r"))]
        csvData = np.array(rawCSV)
        partialXX = np.empty([0, conf.WINDOW_SIZE, conf.PKT_COLUMNS], float)

        # Cut data to fit window and organize them
        i = 0
        while i <= (len(csvData) + 1 - 2 * conf.WINDOW_SIZE):
            # Cut 1th to {conf.PKT_COLUMNS} records of {conf.WINDOW_SIZE} packets
            window = np.dstack(
                np.array(
                    csvData[i:i + conf.WINDOW_SIZE, 1:1 + conf.PKT_COLUMNS]).T)
            partialXX = np.concatenate((partialXX, window), axis=0)
            # Jump to the start point of next window
            i += conf.SLIDE_SIZE

        xx = np.concatenate((xx, partialXX), axis=0)

    # Merge all packets in window to one row
    xx = xx.reshape(len(xx), -1)

    # Process Y
    yCSVPaths = sorted(glob.glob(yPath))
    for csvFile in yCSVPaths:
        print("Processing Y: ", csvFile)

        # Read CSV and prepare temporary variables
        rawCSV = [[float(cell) for cell in line]
                  for line in csv.reader(open(csvFile, "r"))]
        csvData = np.array(rawCSV)
        partialYY = np.zeros(
            ((len(csvData) + 1 - 2 * conf.WINDOW_SIZE) // conf.SLIDE_SIZE + 1,
             conf.N_CLASSES))

        # Parse data and convert them
        i = 0
        while i <= (len(csvData) + 1 - 2 * conf.WINDOW_SIZE):
            # Cut 1th to {conf.WINDOW_SIZE} packets
            window = np.stack(np.array(csvData[i:i + conf.WINDOW_SIZE, 1]))

            # Count each classes
            yRawCount = np.zeros(conf.N_CLASSES)
            for j in range(conf.WINDOW_SIZE):
                yRawCount[int(window[j])] += 1

            # If a class overs zeros
            value = np.zeros(conf.N_CLASSES)
            for j in range(1, conf.N_CLASSES):
                if yRawCount[j] > conf.WINDOW_SIZE * conf.THRESHOLD / 100:
                    value[j] = 1
                    break
            if np.sum(value) == 0:
                value[0] = 2
            partialYY[int(i / conf.SLIDE_SIZE), :] = value

            i += conf.SLIDE_SIZE

        yy = np.concatenate((yy, partialYY), axis=0)

    # Print the results
    print(xx.shape, yy.shape)

    # Return tuple
    return (xx, yy)


def mergeCSV():
    # Check output directory
    mergedDir = conf.MERGED_DIR.format(conf.WINDOW_SIZE, conf.PKT_COLUMNS)
    if os.path.exists(mergedDir):
        print("Old files found. Remove them to continue...")
        shutil.rmtree(mergedDir)
        while os.path.exists(mergedDir):
            pass
    os.makedirs(mergedDir)

    # Calculate and save
    for i, label in enumerate(conf.ACTIONS):
        print("About " + label + " ...")

        # Specify paths
        srcCSIPath = conf.SOURCE_PATH.format("csi", label)
        srcActionPath = conf.SOURCE_PATH.format("action", label)
        mergedCSIPath = conf.MERGED_PATH.format(conf.WINDOW_SIZE,
                                                conf.PKT_COLUMNS, "csi", label)
        mergedActionPath = conf.MERGED_PATH.format(
            conf.WINDOW_SIZE, conf.PKT_COLUMNS, "action", label)

        # Calculate merges
        x, y = mergeCSVOfAction(srcCSIPath, srcActionPath)

        # Save calculated merges
        with open(mergedCSIPath, "w") as outputCSI:
            writer = csv.writer(outputCSI, lineterminator="\n")
            writer.writerows(x)
        with open(mergedActionPath, "w") as outputAction:
            writer = csv.writer(outputAction, lineterminator="\n")
            writer.writerows(y)

        # Finished
        print("==== Action \"" + label + "\" Finished! ====")


def getCSV():
    # Initialize variables
    xByAction = {}
    yByAction = {}

    # Check whether if input directory exists
    if not os.path.exists(conf.MERGED_DIR.format(conf.WINDOW_SIZE, conf.PKT_COLUMNS)):
        print("Input directory not found. Calculate merged CSVs...")
        mergeCSV()
        print("Calculation finished!")

    print("Importing CSV files...")

    # Process by actions
    for b in conf.ACTIONS:

        # If {conf.N_SKIPROW} defined, skip some indexes
        skipIndex = []
        if conf.N_SKIPROW != 0:
            nLines = sum(1 for lines in open(
                conf.MERGED_PATH.format(conf.WINDOW_SIZE, conf.PKT_COLUMNS,
                                        'csi', str(b))))
            skipIndex = [
                x for x in range(1, nLines) if x % conf.N_SKIPROW != 0
            ]

        # Load CSVs
        xx = np.array(
            pd.read_csv(
                conf.MERGED_PATH.format(conf.WINDOW_SIZE, conf.PKT_COLUMNS,
                                        'csi', str(b)),
                header=None,
                skiprows=skipIndex))
        yy = np.array(
            pd.read_csv(
                conf.MERGED_PATH.format(conf.WINDOW_SIZE, conf.PKT_COLUMNS,
                                        'action', str(b)),
                header=None,
                skiprows=skipIndex))

        # Eliminate the NoActivity Data
        rows, cols = np.where(yy > 0)
        xx = np.delete(xx, rows[np.where(cols == 0)], 0)
        yy = np.delete(yy, rows[np.where(cols == 0)], 0)

        xx = xx.reshape(len(xx), conf.WINDOW_SIZE, conf.PKT_COLUMNS)

        # 1000 Hz to 500 Hz (To avoid memory error)
        # xx = xx[:, ::2, :90]

        xByAction[str(b)] = xx
        yByAction[str(b)] = yy

        print(str(b), "finished...", "xx=", xx.shape, "yy=", yy.shape)

    print("Importing finished!")

    return xByAction, yByAction


if __name__ == "__main__":
    mergeCSV()
