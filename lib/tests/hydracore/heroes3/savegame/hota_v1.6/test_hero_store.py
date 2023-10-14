import os
import pytest
import tempfile

from typing import Tuple

from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame, SaveGame
from hydracore.heroes3.model.arch import Color
from hydracore.heroes3.model.hota.hero import HOTAHero
from hydracore.heroes3.model.skill import SkillLevel, Skill
from hydracore.heroes3.model.artifact import Artifacts, Artifact

SAVEGAME = 'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'
HERONAME = 'Ксерон'

def changeable_hero() -> Tuple[SaveGame, HOTAHero]:
    global SAVEGAME, HERONAME
    sg = savegame(Heroes3SaveGameFile(SAVEGAME))
    sg.unpack()
    for hero in sg.heroes():
        if hero.Name == HERONAME:
            return sg, hero

def store_and_back_hero(sg) -> HOTAHero:
    global SAVEGAME, HERONAME
    sg.pack()
    
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, 'packed.gm1')
        sg.file.save(path)
        sgf2 = Heroes3SaveGameFile(path)
        sg2 = savegame(sgf2)
        sg2.unpack()
        for hero in sg2.heroes():
            if hero.Name == HERONAME:
                return hero

def test_hero_primary():
    sg, hero = changeable_hero()
    hero.Attack = 98
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Defense = 98
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.SpellPower = 98
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Knowledge = 98
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()


def test_hero_game_and_map():
    sg, hero = changeable_hero()
    hero.Color = Color.Purple
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Hired = False    
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.X == 20
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Y == 20
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Z == 1
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()


def test_hero_game_and_map():
    sg, hero = changeable_hero()
    hero.Color = Color.Purple
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Hired = False    
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.X == 20
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Y == 20
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Z == 1
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    
def test_hero_properties():
    sg, hero = changeable_hero()
    hero.Level == 25
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Experience == 99999
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.MoveRemain == 1500
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.MoveTotal == 2300
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.SpellPointsRemaining == 100
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()

def test_hero_skills():
    sg, hero = changeable_hero()
    hero.AddSkill(2, Skill('Water Magic', SkillLevel.Basic))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.AddSkill(3, Skill('Ballistics', SkillLevel.Advanced))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.AddSkill(7, Skill('Luck', SkillLevel.Expert))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()


def test_hero_items():
    sg, hero = changeable_hero()
    hero.Ballista = True
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.AmmoCart = True
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.FirstAidTent = True
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Spellbook = False
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.Cannon = False
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()

def test_hero_spells():
    sg, hero = changeable_hero()
    with pytest.raises(RuntimeError):
        hero.AddSpell('Implosion')
        assert hero.hero_state() == store_and_back_hero(sg).hero_state()
        hero.RemoveSpell('Curse')
        assert hero.hero_state() == store_and_back_hero(sg).hero_state()

def test_hero_artifacts():
    sg, hero = changeable_hero()
    hero.TakeOff('helm')
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.PutOn(Artifacts('hota').Get('Crown of the Five Seas'))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    with pytest.raises(RuntimeError):
        hero.PutOn(Artifacts('hota').Get('Helm of Heavenly Enlightenment'))
    hero.PutOn(Artifacts('hota').Get('Tome of Water'))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    with pytest.raises(RuntimeError):
        hero.PutOn(Artifacts('hota').Get('Tome of Water'))
    hero.TakeOff('side1')
    hero.PutOn(Artifact.Scroll('Implosion'))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()

def test_hero_inventory():
    sg, hero = changeable_hero()
    hero.AddToInventory(Artifacts('hota').Get('Angelic Alliance'))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.AddToInventory(Artifact.Scroll('Implosion'))
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()

def test_hero_army():
    sg, hero = changeable_hero()
    hero.AddCreature(1, 'Imp', 1001)
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
    hero.DropCreature(3)
    assert hero.hero_state() == store_and_back_hero(sg).hero_state()
