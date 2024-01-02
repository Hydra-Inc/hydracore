from typing import Pattern

from hydracore.format.heroes3 import Heroes3SaveGameFile

from ..main import _SaveGame
from .patterns import DATE_REGEX, MAP_FILE_REGEX, TITLE_AND_DESCRIPTION_REGEX


class HotaSaveGame(_SaveGame):

    def __init__(self, sg: Heroes3SaveGameFile, verbose: bool = False, ver: str = 'hota'):
        super().__init__(sg, ver, verbose)

    def date_regex(self) -> Pattern[str]:
        return DATE_REGEX
    
    def map_file_location_regex(self) -> Pattern[str]:
        return MAP_FILE_REGEX
    
    def title_and_description_regex(self) -> Pattern[str]:
        return TITLE_AND_DESCRIPTION_REGEX
   

SaveGame = HotaSaveGame
