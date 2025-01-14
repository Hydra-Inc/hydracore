import importlib
import struct
import re

from typing import List, Optional, Pattern

from hydracore.format.heroes3 import Heroes3SaveGameFile

from .hero import SavizableHero
from ..model.hero import Hero
from ..model.game import check_version, to_text
from ..model.time import Date, days_passed
from ..model.map import MapBannedInfo

# ---------------------------------------------------------------- Interface --

class SaveGame:

    def set_configuration(self, mapinfo: MapBannedInfo):
        """
        Sets current game configuration for ability to PACK game back.
        This is required:
          - know which spells are available to this map
          - know which artifacts are available to this map

        We know that from description we may load Template, then map info,
        but this is not our responsibility.
        You should set this externally.
        """
        raise NotImplementedError()

    def check(self) -> bool:
        """
        Checks if the provided binary file is a Heroes3 Save Game file
        """
        raise NotImplementedError()

    def unpack(self):
        """
        Does a main parse loop to locate everything in the provided binary file,
        may try several attempts to run the parsing engine, including,
        search by regex, then search by name and etc...
        """
        raise NotImplementedError()
    
    def pack(self):
        """
        Pack the information the savegame information to SGfile
        """
        raise NotImplementedError()
    
    @property
    def file(self) -> Heroes3SaveGameFile:
        """
        Returns a file object of the save game
        """
        raise NotImplementedError()
    
    # ------------------------------------------------------------- Get info --
    
    def heroes(self) -> List[Hero]:
        """
        Currently supports only this method - extract all Heroes in file

        Should also return Hero object with its location on map and player!
        """
        raise NotImplementedError()

    @property
    def date(self) -> Date:
        """
        Returns a gamedate in format
        """
        raise NotImplementedError()
    
    @property
    def title(self) -> Optional[str]:
        """
        Returns a title of the scenario
        """
        raise NotImplementedError()

    @property
    def description(self) -> Optional[str]:
        """
        Returns a description of the scenario
        """
        raise NotImplementedError()
    
    @property
    def map_file_location(self) -> Optional[str]:
        """
        Returns a map file name
        """
        raise NotImplementedError()
    
    def dump_info(self):
        """
        Dump parsed info
        """
        raise NotImplementedError()


def savegame(sg: Heroes3SaveGameFile, ver: Optional[str] = None, verbose: bool = False) -> SaveGame:
    """
    Creates object of type SaveGame from the binary file.

    sg - opened binary file
    ver - if set - use this version, otherwise detect from file
    """
    return _savegame(sg, ver, verbose=verbose)


# ----------------------------------------------------------- Implementation --

def _savegame(sg: Heroes3SaveGameFile, ver: Optional[str] = None, verbose: bool = False) -> SaveGame:
    if not ver:
        major = sg.data[8]
        minor = sg.data[12]
        if major >= 44 and minor >= 5:
            ver = 'hota'
            HOTA17_TITLE_OFFSET = re.compile(b"""
                H3SVG.{65}...?\x01
            """, re.VERBOSE | re.DOTALL)
            toff = list(sg.regex_search(HOTA17_TITLE_OFFSET))
            if len(toff) >= 1:
                ver = 'hota17'
        else:
            ver = 'sod'
    check_version(ver)
    modname = f'.{ver}.main'
    mod = importlib.import_module(modname, __package__)
    savegame = getattr(mod, 'SaveGame')
    return savegame(sg, verbose=verbose)


class _SaveGame(SaveGame):

    def __init__(self, sg: Heroes3SaveGameFile, ver: str, verbose: bool = False):
        """
        sg - binary file with a Heroes3 Saved game
        """
        self.ver = ver
        self.sgfile = sg
        self.verbose = verbose
        self._heroes = []
        self._version = None
        self._date = None
        self._map_info = None
        self._title = None
        self._description = None
        self._map_file_location = None

    def heroes(self) -> List[Hero]:
        return self._heroes

    def set_configuration(self, mapinfo: MapBannedInfo):
        self._map_info = mapinfo
    
    def unpack(self):
        self.unpack_info()
        self.unpack_heroes()

    def pack(self):
        self.pack_info()
        self.pack_heroes()

    @property
    def file(self) -> Heroes3SaveGameFile:
        return self.sgfile
    
    @property
    def date(self) -> Date:
        return self._date

    def set_date(self, date: Date):
        self._date = date
    
    @property
    def title(self) -> Optional[str]:
        return self._title

    @property
    def description(self) -> Optional[str]:
        return self._description
    
    @property
    def map_file_location(self) -> Optional[str]:
        return self._map_file_location

    def dump_info(self):
        print(f'Version of the Game saved the file is {self._version[0]}.{self._version[1]} ({self.ver})')
        if self._date:
            passed = str(days_passed(self._date))
            print(f'  Month {self._date.month}  Week {self._date.week}  Day {self._date.day},  days passed {passed}')
        else:
            print(f'  Month ???  Week ???  Day ???')
        print(f'  Title: {self._title}')
        print(f'  Description: {self._description}')
        print(f'  Map File: {self._map_file_location}')

    # ------------------------------------------------------- Actual parsers --

    def unpack_info(self):
        """
        Parse general savegame info. We need:
          [+] version
          [+] current day
          [-] template name
          [-] which color is Player
          [-] map file name
          [-] map file location
        """
        # Major and Minor version
        self._version = self.sgfile.data[8], self.sgfile.data[12]

        # Date of the savegame
        date = list(self.sgfile.regex_search(self.date_regex()))
        if len(date) == 1:
            _, m = date[0]
            day = struct.unpack('<B', m.group('day'))[0]
            week = struct.unpack('<B', m.group('week'))[0]
            month = struct.unpack('<B', m.group('month'))[0]
            self._date = Date(int(month), int(week), int(day))
        else:
            self._date = None
            #raise ValueError(f'Cannot locate date in the savegame, found locations: ' + str(len(date)))

        # Title
        tandd = list(self.sgfile.regex_search(self.title_and_description_regex()))
        if len(tandd) != 1:
            raise ValueError(f'Cannot locate title and description in the savegame, found locations: ' + str(len(tandd)))
        _, m = tandd[0]
        self._title = to_text(m.group('title1') if m.group('title1') else (m.group('title2') if m.group('title2') else (m.group('title3') if m.group('title3') else m.group('title4') )))
        self._description = to_text(m.group('description'))

        # Map File
        mapf = list(self.sgfile.regex_search(self.map_file_location_regex()))
        if len(mapf) != 1:
            raise ValueError(f'Cannot locate map file location in the savegame, found locations: ' + str(len(mapf)))
        _, m = mapf[0]
        self._map_file_location = m.group(1).decode('latin-1')
        
        
    def pack_info(self):
        """
        Curretnly not supported
        """
        pass

    def unpack_heroes(self):
        """
        Parses the heroes - using RegEx.

        May be add more techniques, but it looks like working like a charm now.
        """
        self._heroes = []

        self.hero = self._new_hero()
        for chunk, m in self.sgfile.regex_search(self.hero.regex(), self.hero.regex_extra()):
            if self.verbose:
                print(f'Located Hero from {chunk.start} to {chunk.end}')
            hero = self._new_hero()
            hero.set_verbose(self.verbose)
            try:
                hero.unpack(chunk, m)
            except:
                # TODO: fix this problem see bug1 in HotA1.7 tests
                if len(hero.Name)<=1:
                    continue
                raise

            self._heroes.append(hero)

    def pack_heroes(self):
        """
        Write heroes from the read ones
        """
        for hero in self._heroes:
            if hero.nothing_changed():
                continue
            if self.verbose:
                name = hero.Name
                print(f'Hero {name} changed!')
            self.sgfile.patch(hero.pack(self._map_info))

    # --------------------------------------------------------- Misc methods --

    def _new_hero(self) -> SavizableHero:
        modname = f'.{self.ver}.hero'
        mod = importlib.import_module(modname, __package__)
        x = getattr(mod, 'TheSavizableHero')
        return x()


    # -------------------------------------------------------------- Regexes --

    def date_regex(self) -> Pattern[str]:
        """
        Regex to locate the date of the save game
        """
        raise NotImplementedError()
    
    def map_file_location_regex(self) -> Pattern[str]:
        """
        Regex to locate the map file
        """
        raise NotImplementedError()
    
    def title_and_description_regex(self) -> Pattern[str]:
        """
        Regex to locate title
        """
        raise NotImplementedError()

