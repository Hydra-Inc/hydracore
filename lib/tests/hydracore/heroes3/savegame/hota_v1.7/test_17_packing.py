import os
import tempfile

from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.hota.hero import HOTAHero


def changeable_hero(sg) -> HOTAHero:
    for hero in sg.heroes():
        if hero.Name == 'Тодд':
            return hero

def test_savegame_unpack_pack():
    sgf1 = Heroes3SaveGameFile('data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1')
    sg = savegame(sgf1)
    sg.unpack()
    sg.pack()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'packed.gm1')
        sg.file.save(path)
        sgf2 = Heroes3SaveGameFile(path)
        assert sgf1.binary_data == sgf2.binary_data

def test_hero_change_and_back():
    sgf1 = Heroes3SaveGameFile('data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1')
    sg = savegame(sgf1)
    sg.unpack()
    xeron = changeable_hero(sg)
    heroes = list([hero.hero_state() for hero in sg.heroes()])
    prev = xeron.Attack
    xeron.Attack = 99
    sg.pack()
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'packed.gm1')
        sg.file.save(path)
        sgf2 = Heroes3SaveGameFile(path)
        sg2 = savegame(sgf2)
        sg2.unpack()
        heroes2 = list([hero.hero_state() for hero in sg2.heroes()])
        assert heroes != heroes2
        assert xeron.hero_state() == changeable_hero(sg2).hero_state()
        xeron = changeable_hero(sg2)
        xeron.Attack = prev
        sg2.pack()
        with tempfile.TemporaryDirectory() as tmp2:
            path2 = os.path.join(tmp2, 'packed2.gm1')
            sg2.file.save(path2)
            sgf3 = Heroes3SaveGameFile(path2)
            sg3 = savegame(sgf3)
            sg3.unpack()
            heroes3 = list([hero.hero_state() for hero in sg3.heroes()])
            assert heroes == heroes3
