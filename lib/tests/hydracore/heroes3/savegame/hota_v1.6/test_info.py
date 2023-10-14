from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.time import Date
from hydracore.heroes3.model.map import maybe_map_info


def test_savegame_jo_date():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    assert sg.date == Date(2, 1, 1)


def test_savegame_jo_mapfile():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    assert sg.map_file_location == 'Player 2023.05.02 01;08 Jebus Outcast 2.83a.h3m'


def test_savegame_jo_title():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    assert '2023.05.02' in sg.title
    assert 'Jebus Outcast 2.83a' in sg.title


def test_savegame_jo_description():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    assert sg.description == 'Map created by the Random Map Generator. Template was Jebus Outcast from pack Jebus Outcast 2.83a, Random seed was 1682989697, size 144, levels 1, humans 1, computers 3, water None, monsters 3, HotA 1.6.1 expansion map, red is human, red town choice is inferno'


def test_savegame_scenario_date():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_scenario_pered_burej.GM1'))
    sg.unpack()
    assert sg.date == Date(1, 1, 1)


def test_savegame_scenario_mapfile():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_scenario_pered_burej.GM1'))
    sg.unpack()
    assert sg.map_file_location == '[HotA] Before the Storm.h3m'


def test_savegame_scenario_title():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_scenario_pered_burej.GM1'))
    sg.unpack()
    assert 'Перед бурей' in sg.title


def test_savegame_scenario_description():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_scenario_pered_burej.GM1'))
    sg.unpack()
    assert sg.description == 'Восемь владений много лет жили в шатком мире, но разве может быть согласие между столькими соседями на таком маленьком клочке земли? Вот-вот что-то произойдёт, и вам волей-неволей придётся оказаться в центре событий.'

def test_savegame_map_size():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    mapinfo = maybe_map_info(sg.title, sg.description)
    assert mapinfo.Size == 144


