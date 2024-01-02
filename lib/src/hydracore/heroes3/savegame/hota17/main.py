from hydracore.format.heroes3 import Heroes3SaveGameFile

from ..main import _SaveGame
from ..hota.main import HotaSaveGame


class Hota17SaveGame(HotaSaveGame):

    def __init__(self, sg: Heroes3SaveGameFile, verbose: bool = False):
        super().__init__(sg, verbose,  'hota17')
   

SaveGame = Hota17SaveGame
