import importlib

from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional

from .game import check_version


class SkillLevel(Enum):
    Basic = 1
    Advanced = 2
    Expert = 3

    @staticmethod
    def to_str(level: 'SkillLevel'):
        if level == SkillLevel.Basic:
            return 'Basic'
        
        if level == SkillLevel.Advanced:
            return 'Adavanced'
        
        if level == SkillLevel.Expert:
            return 'Expert'


@dataclass
class Skill:
    Name: str
    Level: SkillLevel


SkillPool_ = {}


def Skills(ver: str) -> 'SkillPool':
    check_version(ver)
    global SkillPool_
    if not SkillPool_.get(ver):
        SkillPool_[ver] = SkillPool(ver)
    return SkillPool_[ver]


class SkillPool:
    def __init__(self, ver):
        self.storage = {}
        modname = f'.{ver}.skills'
        mod = importlib.import_module(modname, __package__)
        self.storage = getattr(mod, 'DATA')

    def dump(self, it: Optional[Iterator] = None):
        if not it:
            it = self.All()
        i = 0
        for skill in it:
            print(f'{skill}')
            i+=1
        print(f'Total: {i}')

    def All(self) -> Iterator[str]:
        return iter(self.storage)
    
    def Count(self) -> int:
        return len(self.storage)