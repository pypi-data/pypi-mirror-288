import typing as tp
from math import ceil

import numpy as np
import tensorflow as tf

from ml_exp_comparator.dataset_stores.dataset_store import DatasetStore


class MNISTDatasetStore(DatasetStore):
    x_vals = None
    y_vals = None

    def _prep_data(self, x, y):
        return x/255, self.one_hot_encoding(y)

    @staticmethod
    def one_hot_encoding(values):
        n_values = np.max(values) + 1
        return np.eye(n_values)[values]

    def yield_batches(self, batch_size: int) -> tp.Iterable[tp.Tuple[tp.Any, tp.Any]]:
        assert self.x_vals.shape[0] == self.y_vals.shape[0], "true input and output are not batching"
        for i in range(ceil(self.x_vals.shape[0]/batch_size)):
            start_row = i*batch_size
            end_row = (i+1)*batch_size
            yield self.x_vals[start_row:end_row, :, :], self.y_vals[start_row:end_row, :]


class MNISTTrainDatasetStore(MNISTDatasetStore):
    def __init__(self):
        super().__init__(name='mnist_train')

        (x_train, y_train), _ = tf.keras.datasets.mnist.load_data()
        self.x_vals, self.y_vals = self._prep_data(x_train, y_train)


class MNISTTestDatasetStore(MNISTDatasetStore):
    def __init__(self):
        super().__init__(name='mnist_test')

        _, (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        self.x_vals, self.y_vals = self._prep_data(x_test, y_test)
