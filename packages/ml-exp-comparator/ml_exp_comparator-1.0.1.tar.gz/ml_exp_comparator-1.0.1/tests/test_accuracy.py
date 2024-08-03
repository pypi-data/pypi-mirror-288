from unittest import TestCase

from ml_exp_comparator.metrics_runners.accuracy_metric_runner import AccuracyMetricRunner
from tests.test_utils import TestCaseParams


class TestBinAcc(TestCase):
    def test_calculate(self):
        test_cases = [
            TestCaseParams(
                description='str input values',
                input_params=(['0', '1', '1', '0', '0'], ['0', '0', '0', '1', '1']),
                output_params=(True, False, False, False, False)
            ),
            TestCaseParams(
                description='int input values',
                input_params=((0, 1, 1, 0, 0), (0, 0, 0, 0, 1)),
                output_params=(True, False, False, True, False)
            ),
            TestCaseParams(
                description='bool input values',
                input_params=((True, False, False, True), (False, True, False, True)),
                output_params=(False, False, True, True)
            )
        ]
        for tc in test_cases:
            with self.subTest(tc.description):
                for to, po, correct_output in zip(*tc.input_params, tc.output_params):
                    with self.subTest(tc.description,
                                      true_output=to,
                                      pred_output=po,
                                      correct_output=correct_output):
                        self.assertEqual(correct_output, AccuracyMetricRunner().calculate(to, po))

    def test_agg_calculate(self):
        test_cases = [
            TestCaseParams(
                description='check 1',
                input_params=(True, False, False, False, False),
                output_params=0.2
            ),
            TestCaseParams(
                description='check 2',
                input_params=(True, False, False, True, False),
                output_params=0.4
            ),
            TestCaseParams(
                description='check 3',
                input_params=(False, False, True, True),
                output_params=0.5
            )
        ]
        for tc in test_cases:
            with self.subTest(tc.description):
                self.assertEqual(tc.output_params, AccuracyMetricRunner().calculate_aggregated(tc.input_params))
