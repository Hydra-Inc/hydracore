import json

from typing import Dict, Optional
from random import random, randrange, choices


class RandomTech:

    def __init__(self, flow: Optional[Dict]={}):
        self._flow = flow
        self._counters = {}

    def get(self, value, group: str='main'):
        if self._flow.get(group, None) is None:
            self._flow[group] = []
        if self._counters.get(group, None) is None:
            self._counters[group] = 0
        self._counters[group] += 1
        if len(self._flow[group]) >= self._counters[group]:
            return self._flow[group][self._counters[group]-1]
        self._flow[group].append(value)
        return value

    def float(self, group: str='main'):
        return self.get(random(), group=group)
    
    def int(self, v: int, max: Optional[int]=None, group: str='main'):
        return self.get(randrange(v) if max is None else randrange(v, max+1), group=group)
    
    def weighted_choice(self, mapping: Dict, group: str='main'):
        ch = []
        w = []
        for k, v in mapping.items():
            ch.append(k)
            w.append(v)
        return self.get(choices(ch, w, k=1), group)[0]
    
    def pack(self) -> Dict:
        return {'flow': self._flow, 'counter': self._counters}
    
    def unpack(self, d: Dict):
        self._flow = d['flow']
        self._counters = {}

    def unpack_and_continue(self, d: Dict):
        self._flow = d['flow']
        self._counters = d['counter']

    def save(self, filename: str):
        with open(filename, "w") as f:
            f.write(json.dumps(self.pack()))

    def load(self, filename: str):
        with open(filename, "r") as f:
            self.unpack(json.loads(f.read()))

    def load_and_continue(self, filename: str):
        with open(filename, "r") as f:
            self.unpack_and_continue(json.loads(f.read()))
        