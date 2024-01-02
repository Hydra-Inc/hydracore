from ..hota.towns import DATA as BASE_DATA
from ..hota.towns import HEROCLASSES as BASE_HEROCLASSES
from ..town import Town, HeroClass

# SOD towns and HeroClasses

DATA = []
HEROCLASSES = []

for art in BASE_DATA:
    DATA.append(art)

for art in BASE_HEROCLASSES:
    HEROCLASSES.append(art)


# HOTA town and HeroClass

DATA.append(Town("Factory"))

HEROCLASSES.append(HeroClass('Factory', 'Mercenary', 0))
HEROCLASSES.append(HeroClass('Factory', 'Artificer', 1))
