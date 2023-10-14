from typing import Optional, List

from .base import Trainer, Difficulty
from .list import TrainerList

from ..model.hero import Hero
from ..model.time import Date


def get_trainer(id: str, date: Date, heroes: List[Hero], difficulty: Difficulty) -> Optional[Trainer]:
    """
    Returns a trainer ready to run or None if not found.

    date - savegame date
    heroes - heroes list from the savegame
    difficulty - trainer difficulty to use
    """
    list = TrainerList()
    if not list.has(id):
        return None

    trainer = list.at(id)
    trainer.SetDate(date)
    trainer.SetHeroes(heroes)
    trainer.SetDifficulty(difficulty)

    return trainer
