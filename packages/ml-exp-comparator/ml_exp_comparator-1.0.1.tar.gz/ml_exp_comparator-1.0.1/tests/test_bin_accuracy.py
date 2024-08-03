from unittest import TestCase

from ml_exp_comparator.metrics_runners.bin_accuracy_metric_runner import BinAccuracyMetricRunner
from tests.test_utils import TestCaseParams, TestCompleteRunParams


class TestBinAcc(TestCase):
    def test_calculate(self):
        test_cases = [
            TestCaseParams(
                description='int input values',
                input_params=((0, 1, 1, 0, 0), (0, 0, 0, 1, 1)),
                output_params=('tn', 'fn', 'fn', 'fp', 'fp')
            ),
            TestCaseParams(
                description='bool input values',
                input_params=((True, False, False, True), (False, True, False, True)),
                output_params=('fn', 'fp', 'tn', 'tp')
            ),
            TestCompleteRunParams(
                is_correct=False,
                description='not int or bool input values',
                input_params=((0.1, [2.3], '2.1', {2.}), (0.1, [1.4], '2.1', {1.}))
            )
        ]
        for tc in test_cases:
            if isinstance(tc, TestCaseParams):
                for to, po, correct_output in zip(*tc.input_params, tc.output_params):
                    with self.subTest(tc.description,
                                      true_output=to,
                                      pred_output=po,
                                      correct_output=correct_output):
                        self.assertEqual(correct_output, BinAccuracyMetricRunner().calculate(to, po))
            elif isinstance(tc, TestCompleteRunParams):
                for to, po in zip(*tc.input_params):
                    with self.subTest(tc.description,
                                      true_output=to,
                                      pred_output=po):
                        try:
                            BinAccuracyMetricRunner().calculate(to, po)
                            self.assertTrue(tc.is_correct)
                        except:
                            self.assertFalse(tc.is_correct)

    def test_agg_calculate(self):
        test_cases = [
            TestCaseParams(
                description='check 1',
                input_params=('tn', 'fn', 'fn', 'fp', 'fp'),
                output_params=0.2
            ),
            TestCaseParams(
                description='check 2',
                input_params=('fn', 'fp', 'tn', 'tp'),
                output_params=0.5
            )
        ]
        for tc in test_cases:
            with self.subTest(tc.description):
                self.assertEqual(tc.output_params, BinAccuracyMetricRunner().calculate_aggregated(tc.input_params))
