from hydracore.format.heroes3 import Heroes3SaveGameFile
from hydracore.heroes3.savegame.main import savegame
from hydracore.heroes3.model.arch import Color
from hydracore.heroes3.model.hota.hero import HOTAHero
from hydracore.heroes3.model.skill import SkillLevel


def test_savegame_hero_in():
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    found = False
    for hero in sg.heroes():
        if hero.Name == 'Тодд':
            found = True
    assert found


def testable_hero() -> HOTAHero:
    sg = savegame(Heroes3SaveGameFile(
        'data/heroes3/savegames/hota_v1.7/game_factory_jo_todd.GM1'))
    sg.unpack()
    for hero in sg.heroes():
        if hero.Name == 'Тодд':
            return hero


def test_hero_general_info():
    hero = testable_hero()
    assert hero.Class == 'Artificer'
    assert hero.Town == 'Factory'


def test_hero_primary():
    hero = testable_hero()
    assert hero.Attack == 0
    assert hero.Defense == 16
    assert hero.SpellPower == 15
    assert hero.Knowledge == 3


def test_hero_game_and_map():
    hero = testable_hero()
    assert hero.Color == Color.Red
    assert hero.Hired
    assert hero.X == 124
    assert hero.Y == 22
    assert hero.Z == 0


def test_hero_properties():
    hero = testable_hero()
    assert hero.Level == 10
    assert hero.Experience == 17407
    assert hero.MoveRemain == 0
    assert hero.MoveTotal == 1630
    assert hero.SpellPointsRemaining == 33


def test_hero_skills():
    hero = testable_hero()
    by_slots = {}
    for skill in hero.Skills():
        by_slots[hero.SkillSlot(skill.Name)] = skill
    assert by_slots[1].Level == SkillLevel.Expert and by_slots[1].Name == 'Wisdom'
    assert by_slots[2].Level == SkillLevel.Expert and by_slots[2].Name == 'Tactics'
    assert by_slots[3].Level == SkillLevel.Advanced and by_slots[3].Name == 'Archery'
    assert by_slots[4].Level == SkillLevel.Advanced and by_slots[4].Name == 'Earth Magic'
    assert by_slots[5].Level == SkillLevel.Basic and by_slots[5].Name == 'Offense'
    assert 6 not in by_slots
    assert 7 not in by_slots
    assert 8 not in by_slots


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
    should = ['Bloodlust', 'Shield', 'Dispel', 'Magic Arrow', 'Stone Skin']
    assert set(has) == set(should)


def test_hero_artifacts():
    hero = testable_hero()
    art_by_slot = {slot: hero.ArtifactInSlot(slot) if hero.ArtifactInSlot(
        slot) else None for slot in hero.Slots()}
    assert art_by_slot['helm'] is None
    assert art_by_slot['neck'] is None
    assert art_by_slot['weapon'] is None
    assert art_by_slot['armor'].name == "Titan's Cuirass"
    assert art_by_slot['shield'].name == "Sentinel's Shield"
    assert art_by_slot['lefthand'] is None
    assert art_by_slot['righthand'] is None
    assert art_by_slot['cloak'] is None
    assert art_by_slot['feet'] is None
    assert art_by_slot['side1'].name == 'Runes of Imminency'
    assert art_by_slot['side2'].name == 'Golden Goose'
    assert art_by_slot['side3'].name == "Bowstring of the Unicorns's Mane"
    assert art_by_slot['side4'].name == 'Golden Goose'
    assert art_by_slot['side5'].name == 'Golden Goose'

def test_hero_inventory():
    hero = testable_hero()
    has = [art.name for art in hero.Inventory()]
    should = ['Dragon Scale Shield', 'Sroll spell: View Earth']
    assert set(has) == set(should)


def test_hero_army():
    hero = testable_hero()
    by_slot = {slotid: (creature.name if creature is not None else None, count)
               for slotid, creature, count in hero.Creatures()}
    assert by_slot[1][0] == 'Halfling Grenadier' and by_slot[1][1] == 30
    assert by_slot[2][0] == 'Mechanic' and by_slot[2][1] == 40
    assert by_slot[3][0] == 'Sentinel Automaton' and by_slot[3][1] == 40
    assert by_slot[4][0] == 'Couatl' and by_slot[4][1] == 6
    assert by_slot[5][0] == 'Dreadnought' and by_slot[5][1] == 5
    assert by_slot[6][0] == 'Sandworm' and by_slot[6][1] == 7
    assert by_slot[7][0] == 'Halfling' and by_slot[7][1] == 44
