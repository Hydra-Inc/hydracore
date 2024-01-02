from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame


def test_savegame_load_autover():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'), None)
    assert sg.ver == 'hota17'


def test_savegame_load_hota():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'), 'hota17')
    assert sg.ver == 'hota17'


def test_savegame_unpack():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()


def test_savegame_heroes_count():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    assert len(sg.heroes()) == 198
