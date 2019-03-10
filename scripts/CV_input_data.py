import csv
import glob
import gzip
import os

import numpy as np
import pandas as pd


class DataSet(object):

    def __init__(self, images, labels):
        assert images.shape[0] == labels.shape[0], (
            'images.shape: %s labels.shape: %s' % (images.shape, labels.shape)
        )
        self._num_examples = images.shape[0]
        images = images.reshape(
            images.shape[0], images.shape[1] * images.shape[2])
        self._images = images
        self._labels = labels
        self._epochs_completed = 0
        self._index_in_epoch = 0

    @property
    def images(self):
        return self._images

    @property
    def labels(self):
        return self._labels

    @property
    def num_examples(self):
        return self._num_examples

    @property
    def epochs_completed(self):
        return self._epochs_completed

    def next_batch(self, batch_size):
        start = self._index_in_epoch
        self._index_in_epoch += batch_size
        if self._index_in_epoch > self._num_examples:
            # Finished epoch
            self._epochs_completed += 1
            # Shuffle the data
            perm = np.arange(self._num_examples)
            np.random.shuffle(perm)
            self._images = self._images[perm]
            self._labels = self._labels[perm]
            # Start next epoch
            start = 0
            self._index_in_epoch = batch_size
            assert batch_size <= self._num_examples
        end = self._index_in_epoch
        return self._images[start:end], self._labels[start:end]


def csv_import():
    x_by_behavior = {}
    y_by_behavior = {}
    print("csv file importing...")
    for b in ['sitdown', 'standup', 'to_bad', 'to_good']:
        # Skip every 2 rows -> overlap 800ms to 600ms  (To avoid memory error)
        SKIPROW = 2
        num_lines = sum(1 for l in open("./input/csi_" + str(b) + ".csv"))
        skip_idx = [x for x in range(1, num_lines) if x % SKIPROW != 0]
        xx = np.array(pd.read_csv("./input/csi_" +
                                  str(b) + ".csv", header=None, skiprows=skip_idx))
        yy = np.array(pd.read_csv("./input/behavior_" +
                                  str(b) + ".csv", header=None, skiprows=skip_idx))

        # eliminate the NoActivity Data
        rows, cols = np.where(yy > 0)
        xx = np.delete(xx, rows[np.where(cols == 0)], 0)
        yy = np.delete(yy, rows[np.where(cols == 0)], 0)

        xx = xx.reshape(len(xx), 1000, 90)

        # 1000 Hz to 500 Hz (To avoid memory error)
        xx = xx[:, ::2, :90]

        x_by_behavior[str(b)] = xx
        y_by_behavior[str(b)] = yy

        print(str(b), "finished...", "xx=", xx.shape, "yy=",  yy.shape)

    return x_by_behavior['sitdown'], x_by_behavior['standup'], x_by_behavior['to_bad'], x_by_behavior['to_good'], \
        y_by_behavior['sitdown'], y_by_behavior['standup'], y_by_behavior['to_bad'], y_by_behavior['to_good']
