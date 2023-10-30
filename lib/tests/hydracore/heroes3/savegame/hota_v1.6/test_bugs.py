from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.arch import Color
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


def test_savegame_jo_failed_on_combined_artifact():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_rampart_jo_bug_combart.GM1'))  # d
    sg.unpack()
    main_hero = None
    for hero in sg.heroes():
        if hero.Hired and hero.Color == Color.Red:
            main_hero = hero
            break
    assert main_hero
    assert main_hero.ArtifactInSlot('side1').name == 'Mystic Orb of Mana'
    assert main_hero.ArtifactInSlot('side2').name == 'Golden Goose'
    assert main_hero.ArtifactInSlot('side3').name == 'Bow of Elven Cherrywood'
    assert main_hero.ArtifactInSlot('side4').name == 'Golden Goose'
    assert main_hero.ArtifactInSlot('side5').name == 'Golden Goose'
