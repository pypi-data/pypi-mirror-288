import typing as tp
from dataclasses import dataclass


@dataclass
class TestCompleteRunParams:
    is_correct: bool
    description: str
    input_params: tp.Any


@dataclass
class TestCaseParams:
    description: str
    input_params: tp.Any
    output_params: tp.Any
