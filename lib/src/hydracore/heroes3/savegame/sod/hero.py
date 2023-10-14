from typing import List, Pattern, Dict, Match, Optional

from hydracore.format.chunk import Chunk
from hydracore.heroes3.model.sod.hero import SODHero
from hydracore.heroes3.model.map import MapBannedInfo

from ..hero import _SavizableHero
from .ids import IDs
from .patterns import HERO_REGEX, HERO_OFFSETS, HERO_NAME_OFFSET, HERO_REGEX_EXTRA


class SODHeroSavizable(SODHero, _SavizableHero):

    def serialize(self, map: Optional[MapBannedInfo] = None) -> Chunk:
        raise NotImplementedError()

    def deserialize(self, chunk: Chunk, m: Match):
        raise NotImplementedError()

    @staticmethod
    def regex() -> Pattern[str]:
        return HERO_REGEX

    @staticmethod
    def offset(key: str) -> int:
        return HERO_OFFSETS[key] + HERO_NAME_OFFSET + HERO_REGEX_EXTRA
    
    @staticmethod
    def regex_extra() -> int:
        return HERO_REGEX_EXTRA
    
    @staticmethod
    def id(key: str) -> int:
        if IDs.get(key, None) is None:
            raise RuntimeError(f'Unknown ID for the requested item: {key}')
        return IDs[key]


TheSavizableHero = SODHeroSavizable
