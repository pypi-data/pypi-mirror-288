import typing as tp

from ml_exp_comparator.metrics_runners.metric_runner import MetricRunner


class AccuracyMetricRunner(MetricRunner):
    def __init__(self):
        super().__init__(name='accuracy')

    def calculate(self, true_output: tp.Any, pred_output: tp.Any) -> bool:
        return true_output == pred_output

    def calculate_aggregated(self, single_results: tp.List[bool]) -> float:
        assert all(isinstance(res, bool) for res in single_results)

        return sum(single_results) / len(single_results)
