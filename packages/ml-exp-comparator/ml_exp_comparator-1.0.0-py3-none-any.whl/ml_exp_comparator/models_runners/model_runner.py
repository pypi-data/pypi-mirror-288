import abc
import typing as tp


class ModelRunner(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def run(self, true_input: tp.Any) -> tp.Any:
        pass
