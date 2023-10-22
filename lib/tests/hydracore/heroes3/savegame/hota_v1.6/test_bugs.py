from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.time import Date
from hydracore.heroes3.model.map import maybe_map_info


def test_savegame_jo_date_failed_on_wine_game():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_stronghold_shiva_jo_bad_wine.GM1'))
    sg.unpack()
    assert sg.date == Date(2, 1, 2)


def test_savegame_jo_date_failed_on_wine_game():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_castle_jo_wine.GM1'))  # should be 1,4,7
    sg.unpack()
    assert sg.date == Date(1, 4, 7)
