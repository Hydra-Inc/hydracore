import importlib

from enum import Enum
from dataclasses import dataclass
from typing import Iterator, Optional

from .game import check_version


class MagicSchool(Enum):
    Air = 1
    Earth = 2
    Fire = 3
    Water = 4
    Special = 5

    def to_str(sch: 'MagicSchool'):
        s = str(sch)
        return s.replace('MagicSchool.', "")


SpellId = str


@dataclass
class Spell:
    name: str
    school: MagicSchool
    level: int

    def Air(name: str, level: int):
        return Spell(name, MagicSchool.Air, level)

    def Earth(name: str, level: int):
        return Spell(name, MagicSchool.Earth, level)

    def Fire(name: str, level: int):
        return Spell(name, MagicSchool.Fire, level)

    def Water(name: str, level: int):
        return Spell(name, MagicSchool.Water, level)

    def Special(name: str, level: int):
        return Spell(name, MagicSchool.Special, level)


SpellPool_ = {}


def Spells(ver: str) -> 'SpellPool':
    if ver != 'base':
        check_version(ver)
    global SpellPool_
    if not SpellPool_.get(ver):
        SpellPool_[ver] = SpellPool(ver)
    return SpellPool_[ver]


class SpellPool:
    def __init__(self, ver):
        self.storage = {}
        modname = f'.{ver}.spells'
        mod = importlib.import_module(modname, __package__)
        self.storage = getattr(mod, 'DATA')
        self.by_id = {}
        i = 0
        for spell in self.storage:            
            self.by_id[spell.name] = i
            i += 1
        
    def Get(self, id: SpellId) -> Spell:
        if self.by_id.get(id, None) is None:
            raise RuntimeError(f'Spell {id} not found')
        return self.storage[self.by_id[id]]

    def All(self, all: bool = False) -> Iterator[Spell]:
        for spell in self.storage:
            if not all and spell.level == 0:
                continue
            yield spell

    def Level(self, level: int, iter: Optional[Iterator] = None) -> Iterator[Spell]:
        if iter is None:
            iter = self.All()
        for spell in iter:            
            if spell.level != level:
                continue
            yield spell

    def Air(self, iter: Optional[Iterator] = None) -> Iterator[Spell]:
        if iter is None:
            iter = self.All()
        for spell in iter:
            if spell.school == MagicSchool.Air:
                yield spell

    def Earth(self, iter: Optional[Iterator] = None) -> Iterator[Spell]:
        if iter is None:
            iter = self.All()
        for spell in iter:
            if spell.school == MagicSchool.Earth:
                yield spell

    def Fire(self, iter: Optional[Iterator] = None) -> Iterator[Spell]:
        if iter is None:
            iter = self.All()
        for spell in iter:
            if spell.school == MagicSchool.Fire:
                yield spell

    def Water(self, iter: Optional[Iterator] = None) -> Iterator[Spell]:
        if iter is None:
            iter = self.All()
        for spell in iter:
            if spell.school == MagicSchool.Water:
                yield spell

    def Special(self, iter: Optional[Iterator] = None) -> Iterator[Spell]:
        if iter is None:
            iter = self.All(all=True)
        for spell in iter:
            if spell.school == MagicSchool.Special:
                yield spell

    def dump(self, iter: Optional[Iterator] = None):
        if iter is None:
            iter = self.All()
        i = 0
        for spell in iter:
            sch = MagicSchool.to_str(spell.school)
            print(f'{sch: <7} | LVL {spell.level} | {spell.name}')
            i += 1
        print(f'Total: {i}')
