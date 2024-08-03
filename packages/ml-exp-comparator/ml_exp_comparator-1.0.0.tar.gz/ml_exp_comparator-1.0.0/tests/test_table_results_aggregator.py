import os
import shutil
import unittest

import numpy as np
import pandas as pd

from ml_exp_comparator.results_aggregators.table_results_aggregator import TableResultsAggregator


class TestTableResAgg(unittest.TestCase):
    def test_single_results(self):
        if os.path.exists('.tmp'):
            shutil.rmtree('.tmp')

        resagg = TableResultsAggregator()

        single_metrics_test_cases = [
            ('model1', 'metric1', 'dataset1', 10),
            ('model2', 'metric2', 'dataset1', 9),
            ('model3', 'metric1', 'dataset2', 8)
        ]
        for model_name, metric_name, dataset_name, num_values in single_metrics_test_cases:
            for i in range(num_values):
                resagg.store_single_metric_result(model_name=model_name, metric_name=metric_name,
                                                  dataset_name=dataset_name, result=i)

        for model_name, metric_name, dataset_name, num_values in single_metrics_test_cases:
            with self.subTest(test_method='get_single_metric_results',
                              model_name=model_name, metric_name=metric_name,
                              dataset_name=dataset_name):
                self.assertEqual(list(range(num_values)),
                                 resagg.get_single_metric_results(model_name=model_name, metric_name=metric_name,
                                                                  dataset_name=dataset_name))

        resagg.to_local_store_single_results(single_results_folder='.tmp')
        for model_name, metric_name, dataset_name, num_values in single_metrics_test_cases:
            with self.subTest(test_method='to_local_store_single_results',
                              model_name=model_name, metric_name=metric_name,
                              dataset_name=dataset_name):
                stored_file = f".tmp/{model_name}|{dataset_name}|{metric_name}.txt"
                self.assertTrue(os.path.exists(stored_file))
                with open(stored_file, 'r') as f:
                    lines = f.readlines()
                self.assertEqual(num_values, len(lines))
                for i, stored_value in zip(range(num_values), lines):
                    self.assertEqual(i, int(stored_value.strip()))
        shutil.rmtree('.tmp')

    def test_aggregated_results(self):
        if os.path.exists('.tmp'):
            shutil.rmtree('.tmp')

        resagg = TableResultsAggregator()

        agg_metrics_test_cases = [
            ('model1', 'metric1', 'dataset1', 1),
            ('model1', 'metric2', 'dataset1', 'correct'),
            ('model1', 'metric2', 'dataset2', 0),
            ('model2', 'metric1', 'dataset2', 2.3),
            ('model3', 'metric3', 'dataset3', 'incorrect')
        ]
        for model_name, metric_name, dataset_name, agg_value in agg_metrics_test_cases:
            resagg.store_aggregated_results(model_name=model_name, metric_name=metric_name,
                                            dataset_name=dataset_name, aggregated_result=agg_value)

        stored_file = f".tmp/agg_res.csv"
        resagg.to_local_store_aggregated_results(aggregated_results_path=stored_file)
        self.assertTrue(os.path.exists(stored_file))

        correct_df = pd.DataFrame({
            'metric_name': ['model1', 'model1', 'model2', 'model3'],
            'dataset_name': ['dataset1', 'dataset2', 'dataset2', 'dataset3'],
            'metric1': [1, None, 2.3, None],
            'metric2': ['correct', '0', None, None],
            'metric3': [None, None, None, 'incorrect']
        })

        with self.subTest(test_method='to_local_store_aggregated_results'):
            agg_res = pd.read_csv(stored_file)
            self.assertTrue((agg_res.fillna(value=0).values == correct_df.fillna(value=0).values).all())
        shutil.rmtree('.tmp')
