import typing as tp
from collections import Counter

from ml_exp_comparator.metrics_runners.metric_runner import MetricRunner


class BinAccuracyMetricRunner(MetricRunner):
    def __init__(self):
        super().__init__(name='bin_accuracy')
        self.possible_single_results = {'tp', 'tn', 'fp', 'fn'}

    @staticmethod
    def _check_argument(arg_value: tp.Union[bool, int]) -> None:
        assert isinstance(arg_value, bool) \
               or (isinstance(arg_value, int)
                   and (arg_value == 1 or arg_value == 0)), "incorrect input"

    def calculate(self, true_output: tp.Union[bool, int], pred_output: tp.Union[bool, int]) -> str:
        self._check_argument(true_output)
        self._check_argument(pred_output)

        true_type, false_type = ('tp', 'fn') if true_output == 1 else ('tn', 'fp')
        return true_type if true_output == pred_output else false_type

    def calculate_aggregated(self, single_results: tp.List[str]) -> float:
        assert all(res in self.possible_single_results for res in single_results)

        count_results = Counter(single_results)
        return (count_results['tn'] + count_results['tp'])/sum(count_results.values())
