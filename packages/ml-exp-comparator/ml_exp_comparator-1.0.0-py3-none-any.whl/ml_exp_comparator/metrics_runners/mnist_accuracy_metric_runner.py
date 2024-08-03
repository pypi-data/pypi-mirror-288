import typing as tp

import numpy as np

from ml_exp_comparator.metrics_runners.metric_runner import MetricRunner


class MNISTAccuracyMetricRunner(MetricRunner):
    def __init__(self):
        super().__init__(name='accuracy')

    def calculate(self, true_output: tp.Any, pred_output: tp.Any) -> bool:
        assert true_output.shape == pred_output.shape == (10, )
        true_output_label = np.argmax(true_output)
        pred_output_label = np.argmax(pred_output)
        return true_output_label == pred_output_label

    def calculate_aggregated(self, single_results: tp.List[bool]) -> float:
        assert all(isinstance(res, np.bool_) for res in single_results)

        return sum(single_results) / len(single_results)
