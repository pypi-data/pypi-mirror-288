import abc
import typing as tp


class MetricRunner(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def calculate(self, true_output: tp.Any, pred_output: tp.Any) -> tp.Any:
        pass

    @abc.abstractmethod
    def calculate_aggregated(self, single_results: tp.List[tp.Any]) -> tp.Any:
        pass
