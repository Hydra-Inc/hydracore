from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.arch import Color
from hydracore.heroes3.model.time import Date
from hydracore.heroes3.model.map import maybe_map_info


def test_savegame_jo_failed_a_hero_with_name_len_1():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/bug1_conflux_bad_hero.GM1')) 
    sg.unpack()    
    