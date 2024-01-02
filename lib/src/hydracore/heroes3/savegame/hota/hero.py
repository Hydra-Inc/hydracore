import copy

from typing import Pattern, Match

from hydracore.format.chunk import Chunk
from hydracore.heroes3.model.hota.hero import HOTAHero
from hydracore.heroes3.model.map import MapBannedInfo

from ..base.const import EMPTY_BYTE
from ..hero import _SavizableHero
from .ids import IDs
from .patterns import HERO_REGEX, HERO_OFFSETS, HERO_NAME_OFFSET, HERO_REGEX_EXTRA


from typing import Optional


class BaseHOTAHeroSavizable(_SavizableHero):

    def pack(self, map_info: Optional[MapBannedInfo] = None) -> Chunk:
        """
        Add allowed spells and etc
        """
        if self.nothing_changed():
            return self._chunk
        
        chunk = copy.deepcopy(self._chunk)

        if not self.nothing_changed('main'):
            if self.verbose:
                print('Main info changed')
            self.pack_main(chunk)

        if not self.nothing_changed('game_and_map'):
            if self.verbose:
                print('game_and_map info changed')
            self.pack_game_and_map(chunk)

        if not self.nothing_changed('properties'):
            if self.verbose:
                print('properties info changed')
            self.pack_properties(chunk)

        if not self.nothing_changed('skills'):
            if self.verbose:
                print('skills info changed')
            self.pack_skills(chunk)

        if not self.nothing_changed('items'):
            if self.verbose:
                print('items info changed')
            self.pack_items(chunk)

        if not self.nothing_changed('spells'):
            if self.verbose:
                print('spells info changed')
            if map_info is None:
                raise NotImplementedError('Need to process this path when we know wich spells are banned')
            else:
                self.pack_spells(chunk, map_info.banned_spells())  # not possible as we don't know which
                                          # spells are available in the MAP

        if not self.nothing_changed('artifacts'):
            if self.verbose:
                print('artifacts info changed')
            #raise NotImplementedError('Cant process artifact with spells if we dont know banned spells')
            self.pack_artifacts(chunk)

        if not self.nothing_changed('inventory'):
            if self.verbose:
                print('inventory info changed')
            self.pack_inventory(chunk)

        if not self.nothing_changed('army'):
            if self.verbose:
                print('army info changed')
            self.pack_army(chunk)

        return chunk
        

    def unpack(self, chunk: Chunk, m: Match):
        self.store_chunk(chunk)
        self.unpack_main(chunk, m)
        self.unpack_game_and_map(chunk, m)
        self.unpack_properties(chunk, m)
        self.unpack_skills(chunk, m)
        self.unpack_items(chunk, m)
        self.unpack_spells(chunk, m)
        self.unpack_artifacts(chunk, m)
        self.unpack_inventory(chunk, m)
        self.unpack_army(chunk, m)
        self.store_current_state()
                

    @staticmethod
    def regex() -> Pattern[str]:
        return HERO_REGEX

    @staticmethod
    def offset(key: str) -> int:
        return HERO_OFFSETS[key] + HERO_NAME_OFFSET + HERO_REGEX_EXTRA
    
    @staticmethod
    def regex_extra() -> int:
        return HERO_REGEX_EXTRA
    
    @staticmethod
    def id(key: str) -> int:
        if IDs.get(key, None) is None:
            raise RuntimeError(f'Unknown ID for the requested item: {key}')
        return IDs[key]
    
    def unpack_items(self, chunk: Chunk, m: Match):
        """
        Items: add cannon
        """
        super().unpack_items(chunk, m)
        self.Cannon = True if chunk.to_byte(self.offset('ballista')) == self.id('Cannon') else False


    def pack_items(self, chunk: Chunk):
        """
        Items: ballista, spell book, first aid tent, ammo cart
        """
        super().pack_items(chunk)
        if self.Cannon:
            chunk.put_long(self.id('Cannon'), self.offset('ballista'))
        


class HOTAHeroSavizable(HOTAHero, BaseHOTAHeroSavizable):
    pass


TheSavizableHero = HOTAHeroSavizable
