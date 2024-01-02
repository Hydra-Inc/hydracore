from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.time import Date
from hydracore.heroes3.model.map import maybe_map_info


def test_savegame_jo_date():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    assert sg.date == Date(1, 4, 6)


def test_savegame_jo_mapfile():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    assert sg.map_file_location == 'TechnoCore 2024.01.02 12;07 Jebus Outcast 2.96 test v1.h3m'


def test_savegame_jo_title():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    assert '2024.01.02' in sg.title
    assert 'Jebus Outcast 2.96 test v1' in sg.title


def test_savegame_jo_description():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    assert sg.description == 'Map created by the Random Map Generator. Template was Jebus Outcast 21k from pack Jebus Outcast 2.96 test v1, Random seed was 1704197220, size 144, levels 2, humans 2, computers 2, water None, monsters 4, HotA 1.7.0 expansion map, red is human, red town choice is factory'

def test_savegame_map_size():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    mapinfo = maybe_map_info(sg.title, sg.description)
    assert mapinfo.Size == 144


