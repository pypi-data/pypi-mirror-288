import typing as tp

from ml_exp_comparator.dataset_stores.dataset_store import DatasetStore
from ml_exp_comparator.metrics_runners.metric_runner import MetricRunner
from ml_exp_comparator.models_runners.model_runner import ModelRunner
from ml_exp_comparator.results_aggregators.results_aggregator import ResultsAggregator


class ExperimentsRunner:
    def __init__(self,
                 exp_name: str,
                 storage_folder: str,
                 batch_size: int,
                 exp_models_runners: tp.List[ModelRunner],
                 dataset_store: DatasetStore,
                 metrics_runners: tp.List[MetricRunner],
                 result_aggregator: ResultsAggregator):
        self.exp_name = exp_name
        self.batch_size = batch_size
        self.storage_folder = storage_folder
        self.exp_models_runners = exp_models_runners
        self.dataset_store = dataset_store
        self.metrics_runners = metrics_runners
        self.result_aggregator = result_aggregator

        assert len(self.exp_models_runners) > 0, "No experiment model runners were provided"
        assert len(self.metrics_runners) > 0, "No metrics runners were provided"

    def run_single_model(self, model: ModelRunner):
        for true_batch_input, true_batch_output in self.dataset_store.yield_batches(batch_size=self.batch_size):
            pred_batch_output = model.run(true_batch_input)
            for metric in self.metrics_runners:
                for true_output, pred_output in zip(true_batch_output, pred_batch_output):
                    single_metric_result = metric.calculate(true_output, pred_output)
                    self.result_aggregator.store_single_metric_result(model_name=model.name,
                                                                      metric_name=metric.name,
                                                                      dataset_name=self.dataset_store.name,
                                                                      result=single_metric_result)

        for metric in self.metrics_runners:
            all_single_metric_results = self.result_aggregator.get_single_metric_results(
                model_name=model.name,
                metric_name=metric.name,
                dataset_name=self.dataset_store.name
            )
            aggregated_metric_result = metric.calculate_aggregated(single_results=all_single_metric_results)
            self.result_aggregator.store_aggregated_results(model_name=model.name,
                                                            metric_name=metric.name,
                                                            dataset_name=self.dataset_store.name,
                                                            aggregated_result=aggregated_metric_result)

    def run_models(self):
        for model in self.exp_models_runners:
            self.run_single_model(model)

    def run_and_store(self):
        self.run_models()
        self.result_aggregator.to_local_store(folder=self.storage_folder, exp_name=self.exp_name)
