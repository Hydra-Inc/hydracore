import inspect
import os

from functools import lru_cache
from typing import List

from .base import Trainer


@lru_cache
def list_trainers():
    templates = []
    path = os.path.dirname(os.path.abspath(__file__))
    for subfolder in [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]:
        subpath = os.path.join(path, subfolder)
        for py in [f[:-3] for f in os.listdir(subpath) if f.endswith('.py') and f != '__init__.py' and f != 'list.py']:
            cur = '.'.join(__name__.split('.')[:-1])
            mod = __import__(
                '.'.join([cur, subfolder, py]),
                fromlist=[py])
            classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type) and
                       hasattr(getattr(mod, x), 'trainer')]
            for cls in classes:
                if not inspect.isabstract(cls):
                    templates.append(cls)
    return templates


class TrainerList:

    def __init__(self):
        self.build_list()

    def build_list(self):
        self._all = list_trainers()
        self._extended = {}
        for t in self._all:
            tpl = t()
            self._extended[tpl.id] = {
                'class': t,
                'object': tpl,
                'title': tpl.title
            }

    def get_ids(self) -> List[str]:
        return [x for x in self._extended.keys()]

    def has(self, id: str) -> bool:
        return id in self._extended

    def at(self, id: str) -> Trainer:
        return self._extended[id]['object']
