import logging
import os
from dataclasses import dataclass

import pandas as pd
import typing as tp

from ml_exp_comparator.results_aggregators.results_aggregator import ResultsAggregator

table_res_logger = logging.getLogger('TableResAggLogger')


@dataclass
class TableColumns:
    model_name_col: str = 'model_name'
    dataset_name_col: str = 'dataset_name'


class TableResultsAggregator(ResultsAggregator):
    def __init__(self, *args, **kwargs):
        super().__init__(aggregated_results_file_ext='csv', *args, **kwargs)
        self.single_metrics_store: tp.Dict[str, tp.Dict[str, tp.Dict[str, tp.List[tp.Any]]]] = {}
        self.aggregated_metrics_store: tp.Dict[tp.Tuple[str, str], tp.Dict[str, tp.Union[int, str, float]]] = {}
        self.table_cols_config = TableColumns()

    def store_single_metric_result(self, model_name: str, metric_name: str,
                                   dataset_name: str, result: tp.Any) -> None:
        self.single_metrics_store.setdefault(model_name, {})
        self.single_metrics_store[model_name].setdefault(dataset_name, {})
        self.single_metrics_store[model_name][dataset_name].setdefault(metric_name, [])
        self.single_metrics_store[model_name][dataset_name][metric_name].append(result)

    def get_single_metric_results(self, model_name: str, metric_name: str, dataset_name: str) -> tp.List[tp.Any]:
        return self.single_metrics_store.get(model_name, {}).get(dataset_name, {}).get(metric_name, [])

    def store_aggregated_results(self, model_name: str, metric_name: str,
                                 dataset_name: str, aggregated_result: tp.Union[str, int, float]) -> None:
        self.aggregated_metrics_store.setdefault((model_name, dataset_name), {})
        stored_metrics = self.aggregated_metrics_store[(model_name, dataset_name)]
        assert metric_name not in stored_metrics, f"metric with name {metric_name=} is already stored"
        stored_metrics[metric_name] = aggregated_result

    def to_local_store_single_results(self, single_results_folder: str) -> None:
        os.makedirs(single_results_folder, exist_ok=True)
        for model_name, model_name_results in self.single_metrics_store.items():
            for dataset_name, dataet_results in model_name_results.items():
                for metric_name, metric_results in dataet_results.items():
                    single_results_file_name = f'{model_name}|{dataset_name}|{metric_name}.txt'
                    single_results_full_path = os.path.join(single_results_folder, single_results_file_name)
                    if os.path.exists(single_results_full_path):
                        table_res_logger.error(f'File is already created {single_results_full_path}!!')
                    else:
                        with open(single_results_full_path, 'w') as f:
                            f.write('\n'.join([str(res) for res in metric_results]))

    def get_aggregated_results_df(self):
        all_aggregated_metrics: tp.List[pd.Series] = []

        for (model_name, dataset_name), stored_metrics in self.aggregated_metrics_store.items():
            all_aggregated_metrics.append(pd.Series({
                self.table_cols_config.model_name_col: model_name,
                self.table_cols_config.dataset_name_col: dataset_name,
                **stored_metrics
            }))

        return pd.concat(all_aggregated_metrics, axis=1).T

    def to_local_store_aggregated_results(self, aggregated_results_path: str) -> None:
        os.makedirs(os.path.dirname(aggregated_results_path))
        self.get_aggregated_results_df().to_csv(aggregated_results_path, index=False)
