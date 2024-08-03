import abc
import typing as tp


class DatasetStore(abc.ABC):
    def __init__(self, name: str):
        self.name = name

    @abc.abstractmethod
    def yield_batches(self, batch_size: int) -> tp.Iterable[tp.Tuple[tp.Any, tp.Any]]:
        pass
