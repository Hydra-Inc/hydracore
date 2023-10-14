import importlib
import os

from dataclasses import dataclass, field
from enum import Enum
from typing import Tuple, List, Union, Optional, Iterator


from .game import check_version
from .spell import SpellId
from .arch import Slot

ArtifactId = str

class ArtifactClass(Enum):
    Treasure = 1
    Minor = 2
    Major = 3
    Relic = 4
    Combination = 5
    Scroll = 6

def artclass_to_str(sch: ArtifactClass):
    s = str(sch)
    return s.replace('ArtifactClass.', "")

@dataclass
class Artifact:
    name: str
    slot: Union[Slot, List[Slot]]
    cls: ArtifactClass
    stats: List[int] = field(default_factory=lambda: [0, 0, 0, 0])
    spells: List[SpellId] = field(default_factory=lambda: [])

    @staticmethod
    def New(name: str,
            slot: Union[Slot, List[Slot]],
            cls: ArtifactClass,
            stats: Optional[List[int]] = None,
            spell: Optional[Union[SpellId, List[SpellId]]] = None):
        spells = []
        if spell:
            if isinstance(spell, list):
                spells = spell
            else:
                spells.append(spell)
        return Artifact(
            name=name,
            slot=slot,
            cls=cls,
            stats=[0, 0, 0, 0] if stats else stats,
            spells=spells
        )

    @staticmethod
    def Treasure(name: str,
                 slot: Union[Slot, List[Slot]],
                 stats: Optional[List[int]] = None,
                 spell: Optional[Union[SpellId, List[SpellId]]] = None):
        return Artifact.New(name=name, slot=slot, cls=ArtifactClass.Treasure,
                            stats=stats, spell=spell)

    @staticmethod
    def Minor(name: str,
              slot: Union[Slot, List[Slot]],
              stats: Optional[List[int]] = None,
              spell: Optional[Union[SpellId, List[SpellId]]] = None):
        return Artifact.New(name=name, slot=slot, cls=ArtifactClass.Minor,
                            stats=stats, spell=spell)

    @staticmethod
    def Major(name: str,
              slot: Union[Slot, List[Slot]],
              stats: Optional[List[int]] = None,
              spell: Optional[Union[SpellId, List[SpellId]]] = None):
        return Artifact.New(name=name, slot=slot, cls=ArtifactClass.Major,
                            stats=stats, spell=spell)

    @staticmethod
    def Relic(name: str,
              slot: Union[Slot, List[Slot]],
              stats: Optional[List[int]] = None,
              spell: Optional[Union[SpellId, List[SpellId]]] = None):
        return Artifact.New(name=name, slot=slot, cls=ArtifactClass.Relic,
                            stats=stats, spell=spell)

    @staticmethod
    def Combination(name: str,
                    slot: Union[Slot, List[Slot]],
                    stats: Optional[List[int]] = None,
                    spell: Optional[Union[SpellId, List[SpellId]]] = None):
        return Artifact.New(name=name, slot=slot, cls=ArtifactClass.Combination,
                            stats=stats, spell=spell)

    @staticmethod
    def Scroll(spell: SpellId):
        return Artifact.New(name='Sroll spell: ' + spell, slot=Slot.side,
                            cls=ArtifactClass.Scroll,
                            stats=None, spell=spell)

    def MainSlot(self) -> Slot:
        if isinstance(self.slot, list):
            return self.slot[0]
        return self.slot

    def ExtraSlots(self) -> List:
        if isinstance(self.slot, list):
            return self.slot[1:]
        return []
    
    def AllSlots(self) -> List:
        if isinstance(self.slot, list):
            return self.slot
        return [self.slot]
    
    def Spell(self) -> Optional[SpellId]:
        return self.spells[0] if self.spells else None


ArtifactPool_ = {}
def Artifacts(ver: str) -> 'ArtifactsPool':
    check_version(ver)
    global ArtifactPool_
    if not ArtifactPool_.get(ver):
        ArtifactPool_[ver] = ArtifactsPool(ver)
    return ArtifactPool_[ver]


class ArtifactsPool:
    def __init__(self, ver):
        self.storage = {}        
        modname = f'.{ver}.artifacts'
        mod = importlib.import_module(modname, __package__)
        self.storage = getattr(mod, 'DATA')
        self.map = {}
        i = 0
        for art in self.storage:            
            self.map[art.name] = i
            i += 1

    def All(self) -> Iterator:
        for art in self.storage:
            yield art

    def Treasure(self) -> Iterator:
        for art in self.storage:
            if art.cls == ArtifactClass.Treasure:
                yield art

    def Minor(self) -> Iterator:
        for art in self.storage:
            if art.cls == ArtifactClass.Minor:
                yield art

    def Major(self) -> Iterator:
        for art in self.storage:
            if art.cls == ArtifactClass.Major:
                yield art

    def Relic(self) -> Iterator:
        for art in self.storage:
            if art.cls == ArtifactClass.Relic:
                yield art

    def Combination(self) -> Iterator:
        for art in self.storage:
            if art.cls == ArtifactClass.Combination:
                yield art

    def NotScrolls(self) -> Iterator:
        for art in self.storage:
            if art.cls != ArtifactClass.Scroll:
                yield art

    def Scroll(self) -> Iterator:
        for art in self.storage:
            if art.cls == ArtifactClass.Scroll:
                yield art

    def Slot(self, it: Iterator, slot: str) -> Iterator:
        for art in it:
            sltlst = art.slot
            if not isinstance(sltlst, list):
                sltlst = [sltlst]
            for slt in sltlst:
                if slot == Slot.to_str(slt):
                    yield art

    def Get(self, id: ArtifactId) -> Artifact:
        if self.map.get(id, None) is None:
            raise RuntimeError(f'Wrong artifact name: {id}')
        return self.storage[self.map[id]]

    def dump(self, iter: Optional[Iterator] = None):
        if iter is None:
            iter = self.All()
        i = 0
        for art in iter:
            sch = artclass_to_str(art.cls)
            #stats = of art.sta            
            slots = Slot.to_str(art.slot) if not isinstance(art.slot, list) else ','.join([Slot.to_str(slot) for slot in art.slot])
            spells = ','.join(art.spells)
            
            print(f'{sch: <11} | {art.name: <35} | {slots: <6} | {spells}')
            i += 1
        print(f'Total: {i}')

