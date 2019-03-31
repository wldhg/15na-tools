import numpy as np
import pandas as pd

import Config as conf


def importCSV():
    # Initialize variables
    xByAction = {}
    yByAction = {}

    print("Importing CSV files...")

    # Process by actions
    for b in conf.ACTIONS:

        # If {conf.N_SKIPROW} defined, skip some indexes
        skipIndex = []
        if conf.N_SKIPROW != 0:
            nLines = sum(
                1 for lines in open(conf.MERGED_PATH.format('csi', str(b))))
            skipIndex = [
                x for x in range(1, nLines) if x % conf.N_SKIPROW != 0
            ]

        # Load CSVs
        xx = np.array(
            pd.read_csv(
                conf.MERGED_PATH.format('csi', str(b)),
                header=None,
                skiprows=skipIndex))
        yy = np.array(
            pd.read_csv(
                conf.MERGED_PATH.format('action', str(b)),
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
