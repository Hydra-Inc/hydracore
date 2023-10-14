import importlib

from dataclasses import dataclass
from typing import Iterator, Optional

from .game import check_version


TownId = str


@dataclass
class Town:
    name: str


@dataclass
class HeroClass:
    town: str
    name: str
    type: int  # 0 - warrior, 1 - mage


TownPool_ = {}


def Towns(ver: str) -> 'TownPool':
    check_version(ver)
    global TownPool_
    if not TownPool_.get(ver):
        TownPool_[ver] = TownPool(ver)
    return TownPool_[ver]


class TownPool:
    def __init__(self, ver):
        self.storage = {}
        self.ver = ver
        modname = f'.{ver}.towns'
        mod = importlib.import_module(modname, __package__)
        self.storage = getattr(mod, 'DATA')

        self.hero_classes = getattr(mod, 'HEROCLASSES')

    # --------------------------------------------------------- Town related --

    def dump(self, iter: Optional[Iterator] = None):
        if iter is None:
            iter = self.All()
        i = 0
        for town in iter:
            classes = ', '.join([x.name for x in self.HeroClasses(town.name)])
            print(f'{town.name: <10} | Heroes: {classes}')
            i += 1
        print(f'Total: {i}')

    def All(self) -> Iterator:
        for town in self.storage:
            yield town

    # ---------------------------------------------------- HeroClass related --

    def HeroClasses(self, town: Optional[str] = None) -> Iterator:
        for hc in self.hero_classes:
            if town:
                if hc.town != town:
                    continue
            yield hc

    def TownIdFromHeroClassId(self, HeroclassId : str) -> Optional[TownId]:
        for hc in self.hero_classes:
            if hc.name == HeroclassId:
                return hc.town
        return None

    def dump_heroclasses(self, iter: Optional[Iterator] = None):
        if iter is None:
            iter = self.HeroClasses()
        i = 0
        for hc in iter:
            type = 'Warrior' if hc.type == 0 else 'Mage'
            print(f'{hc.town: <10} | {type: <7} | {hc.name} ')
            i += 1
        print(f'Total: {i}')


    # ------------------------------------------------------------ Creatures --

    def Creatures(self, town: TownId) -> Iterator:
        from .creature import Creatures
        return Creatures(self.ver).Town(town)
