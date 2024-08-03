import typing as tp

import keras

from ml_exp_comparator.models_runners.model_runner import ModelRunner


class SimpleModelRunner(ModelRunner):
    def __init__(self, name, trained_model: keras.Model):
        self.model = trained_model
        super().__init__(name=name)

    def run(self, true_input: tp.Any) -> tp.Any:
        return self.model.predict(true_input)
