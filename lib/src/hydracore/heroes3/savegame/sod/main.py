from typing import Pattern, Dict

from hydracore.format.heroes3 import Heroes3SaveGameFile

from ..main import _SaveGame
from .patterns import HERO_REGEX, HERO_OFFSETS


class SODSaveGame(_SaveGame):

    def __init__(self, sg: Heroes3SaveGameFile, verbose: bool = False):
        super().__init__(sg, 'sod', verbose)

    def hero_regex(self) -> Pattern[str]:
        return HERO_REGEX

    def hero_offsets(self) -> Dict[str, int]:
        return HERO_OFFSETS


SaveGame = SODSaveGame
