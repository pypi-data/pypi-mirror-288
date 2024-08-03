import unittest
from collections import Counter
from itertools import chain

import numpy as np

from ml_exp_comparator.dataset_stores.dataset_store import DatasetStore
from ml_exp_comparator.dataset_stores.mnist_dataset_store import MNISTTrainDatasetStore, MNISTTestDatasetStore


class TestMnist(unittest.TestCase):
    def _test_size(self, ds: DatasetStore, size: int, **kwargs):
        batch_size = 64
        with self.subTest('sizes', **kwargs):
            dataset = list(ds.yield_batches(batch_size))
            self.assertEqual(size, sum(batch[0].shape[0] for batch in dataset))

    def _test_classes_dist(self, ds: DatasetStore, class_portion_eps: float, **kwargs):
        batch_size = 64
        output_values = [np.argwhere(y == 1)[:, 1] for x, y in ds.yield_batches(batch_size)]
        with self.subTest('classes distribution', **kwargs):
            dist_output = Counter(chain(*output_values))
            class_portion = 1 / len(dist_output.keys()) + class_portion_eps
            num_all_outputs = sum(dist_output.values())
            self.assertTrue(all([(class_size / num_all_outputs <= class_portion) for class_size in dist_output.values()]))

    def test_mnist_train(self):
        ds = MNISTTrainDatasetStore()
        self._test_size(ds, size=60000, mnist_ds='train')
        self._test_classes_dist(ds, class_portion_eps=0.05, mnist_ds='train')

    def test_mnist_test(self):
        ds = MNISTTestDatasetStore()
        self._test_size(ds, size=10000, mnist_ds='test')
        self._test_classes_dist(ds, class_portion_eps=0.05, mnist_ds='test')

