import abc
import logging
import os
import typing as tp

res_agg_logger = logging.getLogger('ResultsAggregatorLogger')


class ResultsAggregator(abc.ABC):
    def __init__(self,
                 aggregated_results_file_ext: str,
                 single_results_folder_name: str = 'single_results',
                 aggregated_results_file_name: str = 'aggregated_results'):
        self.single_results_folder_name = single_results_folder_name
        self.aggregated_results_file_name = aggregated_results_file_name
        self.aggregated_results_file_ext = aggregated_results_file_ext
        assert not self.aggregated_results_file_name.endswith(f'.{aggregated_results_file_ext}'), \
            f"remove .{aggregated_results_file_ext} from the file name"

    def _get_single_results_folder(self, folder: str, exp_name: str) -> str:
        return os.path.join(folder, exp_name, self.single_results_folder_name)

    def _get_aggregated_results_path(self, folder: str, exp_name: str) -> str:
        return os.path.join(folder, exp_name, f"{self.aggregated_results_file_name}.{self.aggregated_results_file_ext}")

    @abc.abstractmethod
    def store_single_metric_result(self, model_name: str, metric_name: str,
                                   dataset_name: str, result: tp.Any) -> None:
        pass

    @abc.abstractmethod
    def get_single_metric_results(self, model_name: str, metric_name: str, dataset_name: str) -> tp.List[tp.Any]:
        pass

    @abc.abstractmethod
    def store_aggregated_results(self, model_name: str, metric_name: str,
                                 dataset_name: str, aggregated_result: tp.Any) -> None:
        pass

    @abc.abstractmethod
    def to_local_store_single_results(self, single_results_folder: str) -> None:
        pass

    @abc.abstractmethod
    def to_local_store_aggregated_results(self, aggregated_results_path: str) -> None:
        pass

    def to_local_store(self, folder: str, exp_name: str) -> None:
        self.to_local_store_single_results(self._get_single_results_folder(folder=folder, exp_name=exp_name))
        self.to_local_store_aggregated_results(self._get_aggregated_results_path(folder=folder, exp_name=exp_name))
        res_agg_logger.info("Results are stored into CSV")
