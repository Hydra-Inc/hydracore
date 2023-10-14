from ..sod.towns import DATA as BASE_DATA
from ..sod.towns import HEROCLASSES as BASE_HEROCLASSES
from ..town import Town, HeroClass

# SOD towns and HeroClasses

DATA = []
HEROCLASSES = []

for art in BASE_DATA:
    DATA.append(art)

for art in BASE_HEROCLASSES:
    HEROCLASSES.append(art)


# HOTA town and HeroClass

DATA.append(Town("Cove"))

HEROCLASSES.append(HeroClass('Cove', 'Captain', 0))
HEROCLASSES.append(HeroClass('Cove', 'Navigator', 1))
