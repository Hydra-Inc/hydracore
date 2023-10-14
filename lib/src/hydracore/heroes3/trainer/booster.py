from .base import Trainer


class Booster():
    def __init__(self, trainer: Trainer):
        self._trainer = trainer

    @property
    def Trainer(self) -> Trainer:
        return self._trainer
