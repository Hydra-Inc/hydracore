from abc import ABC, abstractmethod

from hydracore.heroes3.model.hero import Hero

from ..base import Trainer
from ..booster import Booster


class HeroBaseBooster(Booster, ABC):

    @abstractmethod
    def boost(hero: Hero):
        raise NotImplementedError()


class HeroArmyBooster(HeroBaseBooster):
    pass


class HeroSkillsBooster(HeroBaseBooster):
    pass


class HeroArtifactBooster(HeroBaseBooster):
    pass


class HeroSecondariesBooster(HeroBaseBooster):
    pass


class HeroSpellsBooster(HeroBaseBooster):
    pass


class HeroBooster(HeroBaseBooster):

    @abstractmethod
    def setup_boosters(self):
        raise NotImplementedError()

    def __init__(self, trainer: Trainer):
        super().__init__(trainer)
        self._boosters = []
        self.setup_boosters()

    def add_booster(self, booster: HeroBaseBooster):
        self._boosters.append(booster)

    def autoboost(self, hero: Hero):
        for booster in self._boosters:
            booster(self.Trainer).boost(hero)

    def boost(self, hero: Hero):
        self.autoboost(hero)
