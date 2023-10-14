from ..spell import Spell 
from ..base.spells import DATA as BASE_DATA

DATA = []

for art in BASE_DATA:
    DATA.append(art)

DATA.append(Spell.Special("Titan's Lightning Bolt", 0))
