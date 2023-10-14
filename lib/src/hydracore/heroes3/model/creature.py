import importlib

from dataclasses import dataclass, field
from typing import Iterator, Optional

from .game import check_version

from .town import TownId

CreatureId = str

@dataclass
class Creature:
    name: str
    town: TownId
    upg: int         # 0 unupgraded, 1 upgraded, 2 second upgrade
    level: int
    ai_val: int

    # TODO: make this depending on version!
    @staticmethod
    def Castle(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Castle', upg, level, ai_val)

    @staticmethod
    def Rampart(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Rampart', upg, level, ai_val)

    @staticmethod
    def Tower(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Tower', upg, level, ai_val)

    @staticmethod
    def Inferno(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Inferno', upg, level, ai_val)

    @staticmethod
    def Necropolis(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Necropolis', upg, level, ai_val)

    @staticmethod
    def Dungeon(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Dungeon', upg, level, ai_val)

    @staticmethod
    def Stronghold(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Stronghold', upg, level, ai_val)

    @staticmethod
    def Fortress(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Fortress', upg, level, ai_val)

    @staticmethod
    def Conflux(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Conflux', upg, level, ai_val)

    @staticmethod
    def Cove(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Cove', upg, level, ai_val)
    
    @staticmethod
    def Neutral(level: int, upg: int, name: str, ai_val: int):
        return Creature(name, 'Neutral', upg, level, ai_val)


CreaturesPool_ = {}


def Creatures(ver: str) -> 'CreaturesPool':
    check_version(ver)
    global CreaturesPool_
    if not CreaturesPool_.get(ver):
        CreaturesPool_[ver] = CreaturesPool(ver)
    return CreaturesPool_[ver]


class CreaturesPool:
    def __init__(self, ver):
        self.storage = {}
        modname = f'.{ver}.creatures'
        mod = importlib.import_module(modname, __package__)
        self.storage = getattr(mod, 'DATA')
        self.by_town = {}
        self.by_id = {}
        i = 0
        for creature in self.storage:
            if self.by_town.get(creature.town, None) is None:
                self.by_town[creature.town] = []
            self.by_town[creature.town].append(i)
            self.by_id[creature.name] = i
            i += 1

    def dump(self, iter: Optional[Iterator] = None):
        if iter is None:
            iter = self.All()
        i = 0
        for creature in iter:
            upg = ('+' * creature.upg) + (' ' * (2-creature.upg))
            print(f'{creature.town: <10} | LVL {creature.level}{upg} | {creature.name: <20} | AI value: {creature.ai_val} ')
            i += 1
        print(f'Total: {i}')

    def All(self) -> Iterator:
        for creature in self.storage:
            yield creature

    def Level(self, level: int, it: Optional[Iterator] = None) -> Iterator:
        if it is None:
            it = self.All()
        for creature in it:
            if creature.level == level:
                yield creature

    def Upg(self, upg: int, it: Optional[Iterator] = None) -> Iterator:
        if it is None:
            it = self.All()
        for creature in it:
            if creature.upg == upg:
                yield creature

    def Town(self, town: TownId) -> Iterator:
        if self.by_town.get(town, None) is None:
            raise RuntimeError('Bad town id')
        for num in self.by_town[town]:
            yield self.storage[num]

    def Get(self, id: CreatureId) -> Creature:
        if self.by_id.get(id, None) is None:
            raise RuntimeError(f'Bad creature ID={id}')
        return self.storage[self.by_id[id]]



def Level(it: Iterator, level: int) -> Iterator:
    for creature in it:
        if creature.level == level:
            yield creature


def Upgraded(it: Iterator) -> Iterator:
    has_sea_dogs = False
    lst = list(it)
    for creature in lst:
        if creature.name == "Sea Dog":
            has_sea_dogs = True
    
    for creature in lst:
        if creature.upg >= 1:
            if has_sea_dogs and creature.name == "Corsair":
                continue
            yield creature