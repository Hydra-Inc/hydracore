from ..base.towns import DATA as BASE_DATA
from ..base.towns import HEROCLASSES as BASE_HEROCLASSES
from ..town import Town, HeroClass

DATA = []
HEROCLASSES = []

for art in BASE_DATA:
    DATA.append(art)

for art in BASE_HEROCLASSES:
    HEROCLASSES.append(art)


# SOD town and HeroClass

DATA.append(Town("Conflux"))

HEROCLASSES.append(HeroClass('Conflux', 'Planeswalker', 0))
HEROCLASSES.append(HeroClass('Conflux', 'Elementalist', 1))

