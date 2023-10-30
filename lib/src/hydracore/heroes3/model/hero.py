import copy
import importlib

from dataclasses import dataclass
from typing import List, Optional, Union, Dict, Tuple, Iterator

from .arch import Slot, Color, Player
from .artifact import Artifact, ArtifactId, Artifacts, ArtifactClass
from .creature import CreatureId, Creatures, Creature
from .game import check_version
from .skill import Skill, SkillLevel, Skills
from .town import TownId, Towns
from .spell import SpellId, Spell, Spells


# TODO: add all heroes by names
# in all available languages

def new_hero(ver: str):
    check_version(ver)
    modname = f'.{ver}.hero'
    mod = importlib.import_module(modname, __package__)
    return getattr(mod, 'TheHero')


class Hero:
    def __init__(self, ver):
        """
        When adding new fields don't forget to change _init_state method!
        """
        self.ver = ver

        self._name = ''
        self._bio = ''
        self._class = ''
        self._town = ''
        self._specialization = ''

        self._attack = 0
        self._defense = 0
        self._spell_power = 0
        self._knowledge = 0
        self._experience = 0
        self._level = 1
        self._move_total = 0
        self._move_remain = 0
        self._spell_points_remaining = 0

        self._spellbook = False
        self._ammocart = False
        self._ballista = False
        self._first_aid_tent = False

        self._spells = []

        self._skills = {}
        self._skill_slots = {}
        self._init_skill_slots()

        self._slots = {}
        self._init_inventory()
        self._init_slots()

        self._army = {}
        self._init_army()

        self._x = -1
        self._y = -1
        self._z = -1
        self._hired = False

        self._color = None
        self._player = None

        self._stored_full_state = None
        self._init_state()

    # --------------------------------------------------------- General info --

    @property
    def Name(self) -> str:
        return self._name

    @Name.setter
    def Name(self, x: str):
        self._name = x

    @property
    def Bio(self) -> str:
        return self._bio

    @Bio.setter
    def Bio(self, x: str):
        self._bio = x

    @property
    def Class(self) -> str:
        return self._class

    @Class.setter
    def Class(self, x: str):
        self._class = x
        self._town = Towns(self.ver).TownIdFromHeroClassId(self._class)

    @property
    def Town(self) -> TownId:
        return self._town

    @Town.setter
    def Town(self, x: TownId):
        self._town = x

    @property
    def Specialization(self) -> str:
        return self._specialization

    @Specialization.setter
    def Specialization(self, x: str):
        self._specialization = x

    # -------------------------------------------------------------- Primary --

    @property
    def Attack(self) -> int:
        return self._attack

    @Attack.setter
    def Attack(self, x: int):
        self._attack = x

    @property
    def Defense(self) -> int:
        return self._defense

    @Defense.setter
    def Defense(self, x: int):
        self._defense = x

    @property
    def SpellPower(self) -> int:
        return self._spell_power

    @SpellPower.setter
    def SpellPower(self, x: int):
        self._spell_power = x

    @property
    def Knowledge(self) -> int:
        return self._knowledge

    @Knowledge.setter
    def Knowledge(self, x: int):
        self._knowledge = x

    # ---------------------------------------------------------- Exp related --

    @property
    def Experience(self) -> int:
        return self._experience

    @Experience.setter
    def Experience(self, x: int):
        self._experience = x

    @property
    def Level(self) -> int:
        return self._level

    @Level.setter
    def Level(self, x: int):
        self._level = x

    # --------------------------------------------------------- Move related --

    @property
    def MoveTotal(self) -> int:
        return self._move_total

    @MoveTotal.setter
    def MoveTotal(self, x: int):
        self._move_total = x

    @property
    def MoveRemain(self) -> int:
        return self._move_remain

    @MoveRemain.setter
    def MoveRemain(self, x: int):
        self._move_remain = x

    # -------------------------------------------------- Items Non-artifacts --
    @property
    def Spellbook(self) -> bool:
        return self._spellbook

    @Spellbook.setter
    def Spellbook(self, x: bool):
        self._spellbook = x

    @property
    def AmmoCart(self) -> bool:
        return self._ammocart

    @AmmoCart.setter
    def AmmoCart(self, x: bool):
        self._ammocart = x

    @property
    def Ballista(self) -> bool:
        return self._ballista

    @Ballista.setter
    def Ballista(self, x: bool):
        self._ballista = x

    @property
    def FirstAidTent(self) -> bool:
        return self._first_aid_tent

    @FirstAidTent.setter
    def FirstAidTent(self, x: bool):
        self._first_aid_tent = x

    # -------------------------------------------------------- Spell related --
    @property
    def SpellPointsRemaining(self) -> bool:
        return self._spell_points_remaining

    @SpellPointsRemaining.setter
    def SpellPointsRemaining(self, x):
        self._spell_points_remaining = x

    def Spells(self, in_book: bool = True) -> List[Spell]:
        """
        in_book - if True all spells in book else all available spells
        """
        spells_in = [spellid for spellid in self._spells]
        if not in_book:
            for art in self.Artifacts():
                for spell in art.spells:
                    spells_in.append(spell)
        spell_set = set(spells_in)
        return [Spells(self.ver).Get(spellid) for spellid in spell_set]

    def AddSpell(self, spell: SpellId):
        if spell in self._spells:
            return
        self._spells.append(spell)

    def RemoveSpell(self, spell: SpellId):
        if not spell in self._spells:
            return
        self._spells.remove(spell)

    # --------------------------------------------------------------- Skills --

    def _init_skill_slots(self):
        self._skill_slots = {}
        for skill in Skills(self.ver).All():
            self._skill_slots[skill] = None

    def Skills(self) -> List[Skill]:
        return [v for _, v in self._skills.items()]

    def AddSkill(self, slot: int, skill: Skill):
        self._skills[skill.Name] = skill
        self._skill_slots[skill.Name] = slot

    def RemoveSkill(self, skill_name: str):
        if not self._skills.get(skill_name):
            return
        del self._skills[skill_name]
        self._skill_slots[skill_name] = None

    def SkillSlot(self, skill: str) -> Optional[int]:
        return self._skill_slots[skill]

    def SkillLevel(self, skill: str) -> Optional[SkillLevel]:
        if not self._skills.get(skill):
            return None
        return self._skills[skill].Level

    # ----------------------------------------------- Artifacts in inventory --

    def _init_inventory(self):
        self._inventory = []
        for x in range(self.InventorySize()):
            self._inventory.append(None)

    def Inventory(self) -> List[Artifact]:
        return [Artifacts(self.ver).Get(artid) for artid in self._inventory if artid is not None]

    def PlacedInventory(self) -> Iterator[Tuple[int, Artifact]]:
        i = 0
        for artifact in self._inventory:
            i += 1
            if artifact is None:
                continue
            yield i-1, artifact

    def AddToInventory(self, artifact: Artifact, id: Optional[int] = None):
        """
        Raises if no more place left in the inventory
        """
        if id is None:
            id = 0
            for x in self._inventory:
                if x is None:
                    break
                id += 1
            if id == 64:
                raise RuntimeError('No more inventory empty space')
        self._inventory[id] = artifact.name

    def CleanInventory(self):
        self._init_inventory()

    def RemoveFromInventory(self, artifact: Union[ArtifactId, Artifact], all: bool = True):
        """
        artifact - either Artifact id or Artifact
        all - remove all artifacts of this type, else remove only one
        """
        if isinstance(artifact, Artifact):
            artifact = artifact.name
        num = 0
        i = 0
        for art in self._inventory:
            if art == artifact:
                num += 1
                if not all and num >= 2:
                    break
                self._inventory[i] = None
            i += 1

    def InventorySize(self) -> int:
        return 64

    # --------------------------------------------------- Artifacts in slots --

    def _init_slots(self):
        self._slots = {
            'helm':      {'slot': Slot.helm, 'artifact': None, 'blocked': False},
            'neck':      {'slot': Slot.neck, 'artifact': None, 'blocked': False},
            'armor':     {'slot': Slot.armor, 'artifact': None, 'blocked': False},
            'weapon':    {'slot': Slot.weapon, 'artifact': None, 'blocked': False},
            'shield':    {'slot': Slot.shield, 'artifact': None, 'blocked': False},
            'lefthand':  {'slot': Slot.hand, 'artifact': None, 'blocked': False},
            'righthand': {'slot': Slot.hand, 'artifact': None, 'blocked': False},
            'cloak':     {'slot': Slot.cloak, 'artifact': None, 'blocked': False},
            'feet':      {'slot': Slot.feet, 'artifact': None, 'blocked': False},
            'side1':     {'slot': Slot.side, 'artifact': None, 'blocked': False},
            'side2':     {'slot': Slot.side, 'artifact': None, 'blocked': False},
            'side3':     {'slot': Slot.side, 'artifact': None, 'blocked': False},
            'side4':     {'slot': Slot.side, 'artifact': None, 'blocked': False},
            'side5':     {'slot': Slot.side, 'artifact': None, 'blocked': False},
        }

    def Slots(self) -> str:
        return self._slots.keys()

    def _get_avail_slot(self, slot: Slot, slots: Dict) -> Optional[str]:
        for slotname, data in slots.items():
            if data['slot'] != slot:
                continue
            if data['artifact'] or data['blocked']:
                continue
            slots[slotname]['blocked'] = True
            return slotname
        return None

    def _get_avail_exact_slot(self, slot: Slot, slotid: str, slots: Dict) -> Optional[str]:
        data = slots[slotid]
        if data['slot'] != slot:
            return None
        if data['artifact'] or data['blocked']:
            return None
        slots[slotid]['blocked'] = True
        return slotid

    def Artifacts(self) -> List[Artifact]:
        res = []
        for _, d in self._slots.items():
            if d['artifact']:
                res.append(Artifacts(self.ver).Get(d['artifact']))
        return res

    def ArtifactInSlot(self, slot: str) -> Optional[Artifact]:
        if not self._slots[slot]['artifact']:
            return None
        return Artifacts(self.ver).Get(self._slots[slot]['artifact'])

    def PutOn(self, artifact: Artifact, add_spell: bool = False) -> str:
        """
        Raises if this artifact cannot be set to the hero is something is not
        empty among the slots
        """
        ArtifactId = artifact.name
        tempslots = copy.deepcopy(self._slots)
        avail_slot = self._get_avail_slot(artifact.MainSlot(), tempslots)
        if not avail_slot:
            raise RuntimeError(
                f'No available slots to put artifact {artifact.name}')

        extra = artifact.ExtraSlots()
        avail_extra = []
        if extra:
            for slot in extra:
                avail = self._get_avail_slot(slot, tempslots)
                if not avail:
                    raise RuntimeError(
                        f'No available extra slots to put artifact {artifact.name}')
                avail_extra.append(avail)

        self._slots[avail_slot]['artifact'] = ArtifactId
        self._slots[avail_slot]['blocked'] = False
        for extra in avail_extra:
            self._slots[extra]['artifact'] = ArtifactId
            self._slots[extra]['blocked'] = True

        if add_spell:
            for spell in artifact.spells:
                self.AddSpell(spell)
        return avail_slot

    def PutOnSlot(self, slotid: str, artifact: Artifact, add_spell: bool = False) -> str:
        """
        Put the artifact exectly in requested slot
        """
        if not self._slots.get(slotid):
            raise RuntimeError(f'Bad slot provided {slotid}')
        ArtifactId = artifact.name

        tempslots = copy.deepcopy(self._slots)
        avail_slot = self._get_avail_exact_slot(
            artifact.MainSlot(), slotid, tempslots)
        if not avail_slot:
            raise RuntimeError(
                f'No available slots to put artifact {artifact.name}')

        extra = artifact.ExtraSlots()
        avail_extra = []
        if extra:
            for slot in extra:
                avail = self._get_avail_slot(slot, tempslots)
                if not avail:
                    raise RuntimeError(
                        f'No available extra slots to put artifact {artifact.name}')
                avail_extra.append(avail)

        self._slots[avail_slot]['artifact'] = ArtifactId
        self._slots[avail_slot]['blocked'] = False
        for extra in avail_extra:
            self._slots[extra]['artifact'] = ArtifactId
            self._slots[extra]['blocked'] = True

        if add_spell:
            for spell in artifact.spells:
                self.AddSpell(spell)
        return avail_slot

    def PutOnSlotSingle(self, slotid: str, artifact: Artifact, add_spell: bool = False) -> str:
        """
        Put the artifact exectly in requested slot without taking other slots
        for case of Combined artifact
        """
        if not self._slots.get(slotid):
            raise RuntimeError(f'Bad slot provided {slotid}')
        ArtifactId = artifact.name

        tempslots = copy.deepcopy(self._slots)
        avail_slot = self._get_avail_exact_slot(
            artifact.MainSlot(), slotid, tempslots)
        if not avail_slot:
            self.dump()
            raise RuntimeError(
                f'No available slots to put artifact {artifact.name}')

        self._slots[avail_slot]['artifact'] = ArtifactId
        self._slots[avail_slot]['blocked'] = False

        if add_spell:
            for spell in artifact.spells:
                self.AddSpell(spell)
        return avail_slot

    def BlockCombinedArtifacts(self):
        """
        Function to block slots taken by combined artifacts

        Used in case when we unpack hero from savegame, the Golden Goose
        can take side2, side4, side5.. And side3 could be taken
        """

        # check that already propagated the blocking slots
        for slot in self.Slots():
            if self._slots[slot]['blocked']:
                return

        # now process the combined artifacts
        for slot in self.Slots():
            artifact = self.ArtifactInSlot(slot)
            if artifact is None:
                continue
            if artifact.cls != ArtifactClass.Combination:
                continue
            if self._slots[slot]['blocked']:
                continue

            ArtifactId = artifact.name

            tempslots = copy.deepcopy(self._slots)

            extra = artifact.ExtraSlots()
            avail_extra = []
            if extra:
                for slot in extra:
                    avail = self._get_avail_slot(slot, tempslots)
                    if not avail:
                        raise RuntimeError(
                            f'No available extra slots to put artifact {artifact.name}')
                    avail_extra.append(avail)

            for extra in avail_extra:
                self._slots[extra]['artifact'] = ArtifactId
                self._slots[extra]['blocked'] = True

    def _TakeOff(self, slot: str, slots: Dict) -> Optional[ArtifactId]:
        """
        Removes the artifact that is taking requested slot.
        """
        if slots[slot]['artifact'] is None:
            return None
        artifact = slots[slot]['artifact']
        art = Artifacts(self.ver).Get(artifact)

        # locate other location
        if art.cls == ArtifactClass.Combination:
            for slotname, data in slots.items():
                if slotname == slot:
                    continue
                if data['artifact'] == artifact:
                    slots[slotname]['artifact'] = None
                    slots[slotname]['blocked'] = False
        slots[slot]['artifact'] = None
        slots[slot]['blocked'] = False
        return artifact

    def TakeOff(self, slot: str) -> Optional[ArtifactId]:
        return self._TakeOff(slot, self._slots)

    def ForcePutOn(self, artifact: Artifact, add_spell: bool = False) -> List[ArtifactId]:
        """
        Removes all other artifacts that may interfere with this one
        and return a list of removed artifacts ids
        """
        removed = []
        try:
            self.PutOn(artifact, add_spell=add_spell)
        except:
            tempslots = copy.depcopy(self._slots)
            to_remove_slots = []
            for slot in artifact.AllSlots():
                slotname = self._get_avail_slot(slot, tempslots)
                if not slotname:
                    # now lets remove something
                    found = False
                    for slt, data in tempslots:
                        if data['slot'] != slot:
                            continue
                        # already took a slot
                        if data['blocked'] and not data['artifact']:
                            continue
                        found = slt
                        break
                    if not found:
                        raise RuntimeError(
                            f'Cant find a slot for artifact: {artifact.name}. How could be?!')
                    to_remove_slots.append(found)
                    self._TakeOff(found, tempslots)
                else:
                    # found a slot
                    pass
            for aslot in to_remove_slots:
                removed.append(self.TakeOff(aslot))
            self.PutOn(artifact, add_spell=add_spell)
        return removed

    # ------------------------------------------------------------ Creatures --

    def _init_army(self):
        self._army = {
            'slot_1': {'creature': None, 'amount': 0},
            'slot_2': {'creature': None, 'amount': 0},
            'slot_3': {'creature': None, 'amount': 0},
            'slot_4': {'creature': None, 'amount': 0},
            'slot_5': {'creature': None, 'amount': 0},
            'slot_6': {'creature': None, 'amount': 0},
            'slot_7': {'creature': None, 'amount': 0}
        }

    def AddCreature(self, slot: int, creature: CreatureId, amount: int):
        if slot <= 0 or slot > 7:
            raise RuntimeError(f'Bad creature slot {slot}')
        self._army[f'slot_{slot}']['creature'] = creature
        self._army[f'slot_{slot}']['amount'] = amount

    def DropCreature(self, slot: int):
        if slot <= 0 or slot > 7:
            raise RuntimeError(f'Bad creature slot {slot}')
        self._army[f'slot_{slot}']['creature'] = None
        self._army[f'slot_{slot}']['amount'] = 0

    def Creatures(self) -> Iterator[Tuple[int, Creature, int]]:
        i = 0
        for slot, d in self._army.items():
            i += 1
            yield i, None if d['creature'] is None else Creatures(self.ver).Get(d['creature']), d['amount']

    def ComputeArmyValue(self):
        sum = 0
        for _, cr, amount in self.Creatures():
            sum += amount * cr.ai_val
        return sum

    def ArmySlotsCount(self):
        return 7

    def DropAllCreatures(self):
        for n in range(1, self.ArmySlotsCount()+1):
            self.DropCreature(n)

    def FreeArmySlot(self) -> Optional[int]:
        i = 0
        for slot, d in self._army.items():
            i += 1
            if d['creature'] is None:
                return i
        return None

    # --------------------------------------------------------- Game related --
    @property
    def Color(self) -> Optional[Color]:
        return self._color

    @Color.setter
    def Color(self, x: Color):
        self._color = x

    @property
    def Player(self) -> Player:
        return self._player

    @Player.setter
    def Player(self, x: Player):
        self._player = x

    # ---------------------------------------------------------- Map related --

    @property
    def Hired(self) -> bool:
        return self._hired

    @Hired.setter
    def Hired(self, x: bool):
        self._hired = x
        if not x:
            self._x = -1
            self._y = -1
            self._z = -1

    @property
    def X(self) -> int:
        return self._x

    @X.setter
    def X(self, x: int):
        self._hired = True
        self._x = x

    @property
    def Y(self) -> int:
        return self._y

    @Y.setter
    def Y(self, x: int):
        self._hired = True
        self._y = x

    @property
    def Z(self) -> int:
        return self._z

    @Z.setter
    def Z(self, x: int):
        self._hired = True
        self._z = x

    # -------------------------------------------------------------- Dumpers --

    def dump_main(self):
        print(
            f'HERO {self.ver}: {self._name} the {self._class} from {self._town}')

    def dump_game(self):
        clr = Color.to_str(self._color)
        ply = 'Unknown' if self._player is None else Player.to_str(
            self._player)
        print(f'  Color {clr: >7}  | Player: {ply}')

    def dump_map(self):
        if self._hired:
            und = 'Under world' if self._z else 'Up world'
            print(f'  Location: [{self._x: >3}, {self._y: >3}]  {und}')
        else:
            print(f'  Not hired')

    def dump_primary(self):
        print(f'  Attack:      {self._attack: >3}')
        print(f'  Defense:     {self._defense: >3}')
        print(f'  Spell Power: {self._spell_power: >3}')
        print(f'  Knowledge:   {self._knowledge: >3}')

    def dump_exp(self):
        print(
            f'  Level: {self._level: >2}  |  Experience: {self._experience: >7}')

    def dump_moves(self):
        print(f'  Moves: {self._move_remain} out of {self._move_total}')

    def dump_skills(self):
        print('  Skills:')
        i = 1
        for skill in self.Skills():
            lev = SkillLevel.to_str(skill.Level)
            print(f'    Skill {i}: {lev: <10} {skill.Name} ')
            i += 1

    def dump_items(self):
        it = []
        if self._ammocart:
            it.append('Ammo Cart')
        if self._ballista:
            it.append('Ballista')
        if self._first_aid_tent:
            it.append('First Aid Tent')
        if not it:
            it.append('-none-')
        print(f'  Items: '+', '.join(it))

    def dump_spells(self):
        print(f'  Spellbook: ' + ('YES' if self.Spellbook else 'NO ') +
              f' | Spell Points: {self._spell_points_remaining}')
        print(f'  Spells: ' +
              ', '.join([spell.name for spell in self.Spells()]))
        print()

    def dump_artifacts(self):
        print(f'  Artifacts:')
        for slot, d in self._slots.items():
            print(f'     {slot: <9}: ' + (Artifacts(self.ver).Get(
                d['artifact']).name if d['artifact'] else '-'))
        print()

    def dump_inventory(self):
        print(f'  Inventory:')
        i = 0
        for art in self.Inventory():
            i += 1
            print(f'     inv_{i:0>2}: ' + art.name)
        print()

    def dump_army(self):
        print(f'  Army:')
        i = 0
        for slot, d in self._army.items():
            i += 1
            name = Creatures(self.ver).Get(
                d['creature']).name if d['creature'] else '-'
            print(f"     slot_{i}: {name: <25} | {d['amount']}")
        print()

    def dump(self):
        self.dump_main()
        print()
        self.dump_game()
        print()
        self.dump_map()
        print()
        self.dump_primary()
        print()
        self.dump_exp()
        print()
        self.dump_moves()
        print()
        self.dump_skills()
        print()
        self.dump_items()
        print()
        self.dump_spells()
        print()
        self.dump_artifacts()
        print()
        self.dump_inventory()
        print()
        self.dump_army()
        print()

    def dump_short(self):
        self.dump_main()
        self.dump_game()
        self.dump_exp()
        print()

    # ------------------------------------------------------ System methods --

    def get_current_state(self):
        t1 = self._stored_full_state
        self._stored_full_state = None

        t2 = self._stored_states
        self._stored_states = None

        v = copy.deepcopy(self.__dict__)

        self._stored_full_state = t1
        self._stored_states = t2

        return v

    def hero_attrs(self):
        return Hero().__dict__.keys()

    def hero_state(self):
        st = self.get_current_state()
        return {k: st[k] for k in self.hero_attrs()}

    def store_current_state(self):
        self._stored_full_state = self.get_current_state()
        for k, _ in self._stored_states.items():
            for field in self._stored_states[k]['fields']:
                if not field in self._stored_full_state:
                    raise RuntimeError(
                        f'SYSTEM FAILURE! Field {field} not in Hero class')
                self._stored_states[k]['state'][field] = self._stored_full_state[field]

    def nothing_changed(self, group: Optional[str] = None) -> bool:
        """
        Checks that nothing change in all Hero or in a separate group of fields
        """
        cur_state = self.get_current_state()
        if group is None:
            x = self._stored_full_state
            return x == cur_state
        if not self._stored_states.get(group):
            raise RuntimeError(f'Bad state group {group} for Hero')
        cur_group = {}
        for field in self._stored_states[group]['fields']:
            if not field in cur_state:
                raise RuntimeError(
                    f'SYSTEM FAILURE! Field {field} not in Hero class')
            cur_group[field] = cur_state[field]
        return self._stored_states[group]['state'] == cur_group

    def _init_state(self):
        self._stored_states = {
            'main': {
                'fields': ['_name', '_bio', '_class', '_town', '_specialization'],
                'state': {}
            },
            'game_and_map': {
                'fields': ['_x', '_y', '_z', '_hired', '_color', '_player'],
                'state': {}
            },
            'properties': {
                'fields': ['_attack', '_defense', '_spell_power', '_knowledge',
                           '_experience', '_level', '_move_total', '_move_remain',
                           '_spell_points_remaining'],
                'state': {}
            },
            'skills': {
                'fields': ['_skills', '_skill_slots'],
                'state': {}
            },
            'items': {
                'fields': ['_spellbook', '_ammocart', '_ballista', '_first_aid_tent'],
                'state': {}
            },
            'spells': {
                'fields': ['_spells'],
                'state': {}
            },
            'artifacts': {
                'fields': ['_slots'],
                'state': {}
            },
            'inventory': {
                'fields': ['_inventory'],
                'state': {}
            },
            'army': {
                'fields': ['_army'],
                'state': {}
            },
        }


# ------------------------------------------------------------------ Filters --

def FilterByColor(heroes: Iterator[Hero], color: Color) -> Iterator[Hero]:
    for hero in heroes:
        if hero.Color == color:
            yield hero


def MostExperiencedHero(heroes: Iterator[Hero]) -> Optional[Hero]:
    heroes = list(heroes)
    if len(heroes) == 0:
        return None
    max_exp_hero = heroes[0]
    for hero in heroes:
        if hero.Experience > max_exp_hero.Experience:
            max_exp_hero = hero
    return max_exp_hero


def PlayersColors(heroes: Iterator[Hero]) -> List[Color]:
    return list(set([hero.Color for hero in heroes]))
