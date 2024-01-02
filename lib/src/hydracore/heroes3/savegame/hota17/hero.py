from hydracore.heroes3.model.hota17.hero import HOTA17Hero
from ..hota.hero import BaseHOTAHeroSavizable
from .ids import IDs

class HOTA17HeroSavizable(HOTA17Hero, BaseHOTAHeroSavizable):

    @staticmethod
    def id(key: str) -> int:
        if IDs.get(key, None) is None:
            return None
            raise RuntimeError(f'Unknown ID for the requested item: {key}')
        return IDs[key]

TheSavizableHero = HOTA17HeroSavizable
