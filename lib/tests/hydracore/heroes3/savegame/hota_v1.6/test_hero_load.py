from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.arch import Color
from hydracore.heroes3.model.hota.hero import HOTAHero
from hydracore.heroes3.model.skill import SkillLevel


def test_savegame_hero_in():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    found = False
    for hero in sg.heroes():
        if hero.Name == 'Ксерон':
            found = True
    assert found


def testable_hero() -> HOTAHero:
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.6/game_inferno_xeron_jo.GM1'))
    sg.unpack()
    for hero in sg.heroes():
        if hero.Name == 'Ксерон':
            return hero


def test_hero_general_info():
    hero = testable_hero()
    assert hero.Class == 'Demoniac'
    assert hero.Town == 'Inferno'


def test_hero_primary():
    hero = testable_hero()
    assert hero.Attack == 21
    assert hero.Defense == 27
    assert hero.SpellPower == 24
    assert hero.Knowledge == 17


def test_hero_game_and_map():
    hero = testable_hero()
    assert hero.Color == Color.Red
    assert hero.Hired
    assert hero.X == 23
    assert hero.Y == 28
    assert hero.Z == 0


def test_hero_properties():
    hero = testable_hero()
    assert hero.Level == 19
    assert hero.Experience == 72225
    assert hero.MoveRemain == 1472
    assert hero.MoveTotal == 2400
    assert hero.SpellPointsRemaining == 228


def test_hero_skills():
    hero = testable_hero()
    by_slots = {}
    for skill in hero.Skills():
        by_slots[hero.SkillSlot(skill.Name)] = skill
    assert by_slots[1].Level == SkillLevel.Expert and by_slots[1].Name == 'Leadership'
    assert by_slots[2].Level == SkillLevel.Expert and by_slots[2].Name == 'Tactics'
    assert by_slots[3].Level == SkillLevel.Expert and by_slots[3].Name == 'Earth Magic'
    assert by_slots[4].Level == SkillLevel.Expert and by_slots[4].Name == 'Logistics'
    assert by_slots[5].Level == SkillLevel.Advanced and by_slots[5].Name == 'Wisdom'
    assert by_slots[6].Level == SkillLevel.Expert and by_slots[6].Name == 'Fire Magic'
    assert by_slots[7].Level == SkillLevel.Basic and by_slots[7].Name == 'Air Magic'
    assert by_slots[8].Level == SkillLevel.Advanced and by_slots[8].Name == 'Offense'


def test_hero_items():
    hero = testable_hero()
    assert not hero.Ballista
    assert not hero.AmmoCart
    assert not hero.FirstAidTent
    assert hero.Spellbook
    assert not hero.Cannon


def test_hero_spells():
    hero = testable_hero()
    has = [spell.name for spell in hero.Spells()]
    should = ['Curse', 'Protection from Fire', 'Town Portal', 'Stone Skin',
              'View Air', 'Magic Arrow', 'Bloodlust', 'View Earth', 'Berserk', 'Dispel']
    assert set(has) == set(should)


def test_hero_artifacts():
    hero = testable_hero()
    art_by_slot = {slot: hero.ArtifactInSlot(slot) if hero.ArtifactInSlot(
        slot) else None for slot in hero.Slots()}
    assert art_by_slot['helm'].name == 'Helm of Heavenly Enlightenment'
    assert art_by_slot['neck'] is None
    assert art_by_slot['shield'].name == 'Shield of the Damned'
    assert art_by_slot['lefthand'].name == 'Ring of Life'
    assert art_by_slot['righthand'] is None
    assert art_by_slot['cloak'].name == 'Angel Wings'
    assert art_by_slot['feet'].name == 'Sandals of the Saint'
    assert art_by_slot['side1'] is None
    assert art_by_slot['side2'].name == 'Tome of Air'
    assert art_by_slot['side3'].name == 'Tome of Fire'
    assert art_by_slot['side4'].name == 'Tome of Earth'
    assert art_by_slot['side5'].name == 'Vial of Lifeblood'


def test_hero_inventory():
    hero = testable_hero()
    has = [art.name for art in hero.Inventory()]
    should = ['Sroll spell: Bless', "Titan's Gladius",
              'Golden Goose', 'Cornucopia']
    assert set(has) == set(should)


def test_hero_army():
    hero = testable_hero()
    by_slot = {slotid: (creature.name if creature is not None else None, count)
               for slotid, creature, count in hero.Creatures()}
    assert by_slot[1][0] == None
    assert by_slot[2][0] == None
    assert by_slot[3][0] == 'Devil' and by_slot[3][1] == 26
    assert by_slot[4][0] == 'Efreet Sultan' and by_slot[4][1] == 26
    assert by_slot[5][0] == None
    assert by_slot[6][0] == None
    assert by_slot[7][0] == None
