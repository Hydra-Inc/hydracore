from typing import Pattern, Match, Optional, List

from .base.const import EMPTY_BYTE, EMPTY_SHORT, EMPTY_LONG, NULL_BYTE
from ..model.hero import Hero

from hydracore.utils.misc import strip_name
from hydracore.format.chunk import Chunk
from hydracore.heroes3.model.map import MapBannedInfo
from hydracore.heroes3.model.arch import Color
from hydracore.heroes3.model.artifact import Artifacts, Artifact, ArtifactClass
from hydracore.heroes3.model.creature import Creatures
from hydracore.heroes3.model.game import auto_detect_language, detect_language, \
    to_name, from_name
from hydracore.heroes3.model.skill import Skills, Skill, SkillLevel
from hydracore.heroes3.model.spell import Spells, SpellId
from hydracore.heroes3.model.town import Towns

# ---------------------------------------------------------------- Interface --


class SavizableHero(Hero):

    def pack(self, map_info: Optional[MapBannedInfo] = None) -> Chunk:
        """
        Serializes Hero to a SaveGame format
        """
        raise NotImplementedError()

    def unpack(self, chunk: Chunk, m: Match):
        """
        Deserializes Hero from a SaveGame format
        """
        raise NotImplementedError()
    
    def set_verbose(self, verbose: bool):
        self.verbose = verbose


# ----------------------------------------------------------- Implementation --

class _SavizableHero(SavizableHero):

    @staticmethod
    def id(key: str) -> int:
        """
        Returns an in-game ID of the field
        """
        raise NotImplementedError()

    @staticmethod
    def offset(key: str) -> int:
        """
        Returns an offset of the field
        """
        raise NotImplementedError()

    @staticmethod
    def regex() -> Pattern[str]:
        """
        Regular expression of the Hero regex to match in file
        """
        raise NotImplementedError()

    @staticmethod
    def regex_extra() -> int:
        """
        How much extra bytes to take for regex search.
        Mostly needed for debug purposes and searching something in the memory.
        """
        raise NotImplementedError()

    @property
    def chunk(self):
        """
        Returns the chunk with data
        """
        return self._chunk

    def store_chunk(self, chunk: Chunk):
        """
        Store chunks so we may later use it to serialize Hero
        as some of the binary data should be the same as arrived
        """
        self._chunk = chunk

    def unpack_main(self, chunk: Chunk, m: Match):
        """
        Name of the Hero, plus try to detect the language
        """
        name = strip_name(m.group("name"))
        if auto_detect_language():
            detect_language(name)
        self.Name = to_name(name)

    def pack_main(self, chunk: Chunk):
        chunk.put_str(from_name(self.Name), self.offset('name'), 12)

    def unpack_game_and_map(self, chunk: Chunk, m: Match):
        """
        Game related stuff
        """
        clrval = chunk.to_byte(self.offset('color'))
        if clrval == EMPTY_BYTE:
            self.Color = None
        else:
            colorset = False
            for color in Color:
                if self.id(Color.to_str(color)) == clrval:
                    self.Color = color
                    colorset = True
                    break
            if not colorset:
                raise RuntimeError(f'Cannot identify hero color: {clrval}')
        heroset = False
        hcval = chunk.to_byte(self.offset('heroclass'))
        for heroclass in Towns(self.ver).HeroClasses():
            if self.id(heroclass.name) == hcval:
                self.Class = heroclass.name
                heroset = True
                break
        if not heroset:
            raise RuntimeError(f'Cannot identify hero class: {hcval}')

        if chunk.to_short(self.offset('x')) == EMPTY_SHORT:
            self.Hired = False
        else:
            self.X = chunk.to_short(self.offset('x'))
            self.Y = chunk.to_short(self.offset('y'))
            self.Z = chunk.to_short(self.offset('z'))

    def pack_game_and_map(self, chunk: Chunk):
        """
        Game related stuff
        """
        if self.Color is None:
            chunk.put_byte(EMPTY_BYTE, self.offset('color'))
        else:
            chunk.put_byte(self.id(Color.to_str(self.Color)),
                           self.offset('color'))

        chunk.put_byte(self.id(self.Class), self.offset('heroclass'))

        if not self.Hired:
            chunk.put_short(EMPTY_SHORT, self.offset('x'))
            chunk.put_short(EMPTY_SHORT, self.offset('y'))
            chunk.put_short(EMPTY_SHORT, self.offset('z'))
        else:
            chunk.put_short(self.X, self.offset('x'))
            chunk.put_short(self.Y, self.offset('y'))
            chunk.put_short(self.Z, self.offset('z'))

    def unpack_properties(self, chunk: Chunk, m: Match):
        """
        Main properties - primary skills, exp, level, move points, mana
        """
        self.Attack = chunk.to_byte(self.offset('attack'))
        self.Defense = chunk.to_byte(self.offset('defense'))
        self.SpellPower = chunk.to_byte(self.offset('power'))
        self.Knowledge = chunk.to_byte(self.offset('knowledge'))

        self.Level = chunk.to_byte(self.offset('level'))
        self.Experience = chunk.to_long(self.offset('exp'))

        self.MoveRemain = chunk.to_long(self.offset('movement_left'))
        self.MoveTotal = chunk.to_long(self.offset('movement_total'))

        self.SpellPointsRemaining = chunk.to_short(self.offset('mana'))

    def pack_properties(self, chunk: Chunk):
        """
        Main properties - primary skills, exp, level, move points, mana
        """
        chunk.put_byte(self.Attack, self.offset('attack'))
        chunk.put_byte(self.Defense, self.offset('defense'))
        chunk.put_byte(self.SpellPower, self.offset('power'))
        chunk.put_byte(self.Knowledge, self.offset('knowledge'))

        chunk.put_byte(self.Level, self.offset('level'))
        chunk.put_long(self.Experience, self.offset('exp'))

        chunk.put_long(self.MoveRemain, self.offset('movement_left'))
        chunk.put_long(self.MoveTotal, self.offset('movement_total'))

        chunk.put_short(self.SpellPointsRemaining, self.offset('mana'))

    def unpack_skills(self, chunk: Chunk, m: Match):
        """
        Hero skills with level
        """
        # chunk.dump('heroesx/' + self.Name + '.dat', self.offset('inventory'), self.offset('inventory') + 512)
        skill_count = chunk.to_byte(self.offset('skills_count'))
        if skill_count > 50:
            raise ValueError(f'Too much skills in hero {skill_count} strange!')
        for skill in Skills(self.ver).All():
            skillid = self.id(skill)
            level = chunk.to_byte(self.offset('skills_level')+skillid)
            slot = chunk.to_byte(self.offset('skills_slot')+skillid)
            if not level:
                continue
            if not slot:
                continue
            if slot > skill_count:
                continue
            self.AddSkill(slot, Skill(skill, SkillLevel(level)))

    def pack_skills(self, chunk: Chunk):
        """
        Hero skills with level
        """
        skill_count = len(self.Skills())
        chunk.put_byte(skill_count, self.offset('skills_count'))

        for skill in Skills(self.ver).All():
            level = self.SkillLevel(skill)
            skillid = self.id(skill)
            if level is None:
                chunk.put_byte(NULL_BYTE, self.offset('skills_level')+skillid)
                chunk.put_byte(NULL_BYTE, self.offset('skills_slot')+skillid)
            else:
                slot = self.SkillSlot(skill)
                chunk.put_byte(level.value, self.offset(
                    'skills_level')+skillid)
                chunk.put_byte(slot, self.offset('skills_slot')+skillid)

    def unpack_items(self, chunk: Chunk, m: Match):
        """
        Items: ballista, spell book, first aid tent, ammo cart
        """
        self.Ballista = True if chunk.to_byte(self.offset(
            'ballista')) == self.id('Ballista') else False
        self.AmmoCart = True if chunk.to_byte(
            self.offset('ammo')) == self.id("Ammo Cart") else False
        self.FirstAidTent = True if chunk.to_byte(
            self.offset('tent')) == self.id("First Aid Tent") else False
        self.Spellbook = True if chunk.to_byte(self.offset(
            'spellbook')) == self.id("Spellbook") else False

    def pack_items(self, chunk: Chunk):
        """
        Items: ballista, spell book, first aid tent, ammo cart
        """
        chunk.put_long(
            self.id('Ballista') if self.Ballista else EMPTY_LONG, self.offset('ballista'))
        chunk.put_long(self.id('Ammo Cart')
                       if self.AmmoCart else EMPTY_LONG, self.offset('ammo'))
        chunk.put_long(self.id('First Aid Tent')
                       if self.FirstAidTent else EMPTY_LONG, self.offset('tent'))
        chunk.put_long(self.id(
            'Spellbook') if self.Spellbook else EMPTY_LONG, self.offset('spellbook'))

    def unpack_spells(self, chunk: Chunk, m: Match):
        """
        Spells available to Hero
        """
        for spell in Spells(self.ver).All(True):
            if chunk.to_byte(self.offset('spells_book') + self.id(spell.name)):
                self.AddSpell(spell.name)

    def pack_spells(self, chunk: Chunk, banned_spells: Optional[List[SpellId]] = None):
        """
        Spells available to Hero
        """
        spells_in_book = {spell.name: 1 for spell in self.Spells(in_book=True)}
        spells_avail = {spell.name: 1 for spell in self.Spells(in_book=False)}
        
        # TODO: test avail spells
        for spell in Spells(self.ver).All():
            if spell in banned_spells:
                continue
            chunk.put_byte(1 if spells_in_book.get(spell.name) else 0,
                           self.offset('spells_book') + self.id(spell.name))
            chunk.put_byte(1 if spells_avail.get(spell.name) else 0, self.offset(
                'spells_available') + self.id(spell.name))

    def unpack_artifacts(self, chunk: Chunk, m: Match):
        """
        Artifacts that our hero wears on, the inventory is done in a separate
        method below
        """
        artid_to_name = {}
        for artifact in Artifacts(self.ver).NotScrolls():
            artid_to_name[self.id(artifact.name)] = artifact.name

        spellid_to_name = {}
        for spell in Spells(self.ver).All():
            spellid_to_name[self.id(spell.name)] = spell.name

        scroll_id = self.id("Spell Scroll")
        for slot in self.Slots():

            # check whether it is a scroll or not
            artid = chunk.to_long(self.offset(slot))
            if artid == scroll_id:
                # get spell offset
                spellid = chunk.to_long(self.offset(slot) + 4)
                if spellid_to_name.get(spellid) is None:
                    if spellid != EMPTY_LONG and spellid != 0:
                        raise ValueError(
                            f'Unkown spell 0x{spellid:04X} in Scroll which is not empty and not known')
                    continue

                # Here we rely that we loop over slot in ORDER
                # and PutOn also loop the slots in same ORDER
                # so the scroll will be on SAME "side*" slot as in hero
                artifact = Artifact.Scroll(spellid_to_name.get(spellid))

            else:
                if artid_to_name.get(artid) is None:
                    if artid != EMPTY_LONG and artid != 0:
                        raise ValueError(
                            f'Unkown artifact 0x{artid:04X} which is not empty and not known')
                    continue

                # locate the artifact and put in on hero
                artifact = Artifacts(self.ver).Get(artid_to_name.get(artid))

            slotid = self.PutOnSlot(slot, artifact)
            if slotid != slot:
                raise RuntimeError(
                    f"We've put an artifact {artifact.name} in slot {slotid}, but parsed in on slot {slot}")

    def pack_artifacts(self, chunk: Chunk):
        """
        Artifacts that our hero wears on, the inventory is done in a separate
        method below
        """
        scroll_id = self.id("Spell Scroll")

        for slot in self.Slots():
            art = self.ArtifactInSlot(slot)
            if art:
                if art.cls != ArtifactClass.Scroll:
                    chunk.put_long(self.id(art.name), self.offset(slot))
                    chunk.put_long(EMPTY_LONG, self.offset(slot) + 4)
                else:
                    chunk.put_long(scroll_id, self.offset(slot))
                    spellname = Spells(self.ver).Get(art.spells[0]).name
                    chunk.put_long(self.id(spellname), self.offset(slot) + 4)
            else:
                chunk.put_long(EMPTY_LONG, self.offset(slot))
                chunk.put_long(EMPTY_LONG, self.offset(slot)+4)


    def unpack_inventory(self, chunk: Chunk, m: Match):
        """
        Artifacts that our hero wears in the inventory
        """
        artid_to_name = {}
        for artifact in Artifacts(self.ver).NotScrolls():
            artid_to_name[self.id(artifact.name)] = artifact.name

        spellid_to_name = {}
        for spell in Spells(self.ver).All():
            spellid_to_name[self.id(spell.name)] = spell.name

        scroll_id = self.id("Spell Scroll")

        for invnum in range(self.InventorySize()):
            # check whether it is a scroll or not
            # print(self.Name, 'Data', invnum, self.offset('inventory') + invnum)
            artid = chunk.to_long(self.offset('inventory') + invnum * 8)

            if artid == scroll_id:
                # get spell offset
                spellid = chunk.to_long(
                    self.offset('inventory') + invnum * 8 + 4)
                if spellid_to_name.get(spellid) is None:
                    if spellid != EMPTY_LONG and spellid != 0:
                        raise ValueError(
                            f'Unkown spell 0x{spellid:04X} in Scroll which is not empty and not known')
                    continue

                # Here we rely that we loop over slot in ORDER
                # and PutOn also loop the slots in same ORDER
                # so the scroll will be on SAME "side*" slot as in hero
                artifact = Artifact.Scroll(spellid_to_name.get(spellid))

            else:
                if artid_to_name.get(artid) is None:
                    if artid != EMPTY_LONG and artid != 0:
                        raise ValueError(
                            f'Unkown artifact 0x{artid:04X} which is not empty and not known')
                    continue

                # locate the artifact and put in on hero
                artifact = Artifacts(self.ver).Get(artid_to_name.get(artid))

            self.AddToInventory(artifact, invnum)

    def pack_inventory(self, chunk: Chunk):
        """
        Artifacts that our hero wears in the inventory
        """
        scroll_id = self.id("Spell Scroll")
        mapped = { k: Artifacts(self.ver).Get(v) for k,v in self.PlacedInventory() }

        for invnum in range(self.InventorySize()):
            if mapped.get(invnum):
                artifact = mapped.get(invnum)
                if artifact.cls != ArtifactClass.Scroll:
                    chunk.put_long(self.id(artifact.name), self.offset('inventory') + invnum * 8)
                    chunk.put_long(EMPTY_LONG, self.offset('inventory') + invnum * 8 + 4)
                else:
                    chunk.put_long(scroll_id, self.offset('inventory') + invnum * 8)
                    spellname = Spells(self.ver).Get(artifact.spells[0])
                    chunk.put_long(self.id(spellname.name), self.offset('inventory') + invnum * 8 + 4)
            else:
                chunk.put_long(EMPTY_LONG, self.offset('inventory') + invnum * 8)
                chunk.put_long(EMPTY_LONG, self.offset('inventory') + invnum * 8 + 4)


    def unpack_army(self, chunk: Chunk, m: Match):
        """
        Obtain Creatures to the Hero
        """
        creatureid_to_name = {}
        for creature in Creatures(self.ver).All():
            creatureid_to_name[self.id(creature.name)] = creature.name

        for slot in range(self.ArmySlotsCount()):
            armid = chunk.to_long(self.offset('army_types') + slot * 4)
            armcnt = chunk.to_long(self.offset('army_counts') + slot * 4)

            if creatureid_to_name.get(armid) is None:
                if armid != EMPTY_LONG and armid != 0:
                    raise ValueError(
                        f'Unkown creature 0x{armid:04X} which is not empty and not known')
                continue

            self.AddCreature(slot+1, creatureid_to_name.get(armid), armcnt)


    def pack_army(self, chunk: Chunk):
        """
        Obtain Creatures to the Hero
        """
        for slotid, creature, count in self.Creatures():
            slotid -= 1
            if creature is not None:
                chunk.put_long(self.id(creature.name), self.offset('army_types') + slotid * 4)
                chunk.put_long(count, self.offset('army_counts') + slotid * 4)
            else:
                chunk.put_long(EMPTY_LONG, self.offset('army_types') + slotid * 4)
                chunk.put_long(EMPTY_LONG, self.offset('army_counts') + slotid * 4)