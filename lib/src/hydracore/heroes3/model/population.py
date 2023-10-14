import math

from enum import Enum

from .time import Date


class FortType(Enum):
    Fort = 1
    Citadel = 2
    Castle = 3
    

BASE_APPROX = {
    1: 15,
    2: 8,
    3: 7,
    4: 4,
    5: 3,
    6: 2,
    7: 1
}

def approx_population_grow_per_week_in_town(level: int,
                                            fort_type: FortType,            
                                            external_dwellings: int,
                                            grail: bool=False,
                                            legion_statue: bool=False
                                            ) -> int:
    """
    Approximate growth of population of a level in castle, could be used 
    to approximately estimate the expected army of the hero.
    """
    global BASE_APPROX
    COEF = {
        FortType.Fort: 1,
        FortType.Citadel: 1.5,
        FortType.Castle: 2
    }

    LegionPartsCoef = 0         # unsupported for approx mode
    ExtraInCastleDwellings = 0  # unsupported for approx mode
    Week = 0                    # unsupported for approx mode
    
    return math.floor( BASE_APPROX[level] * COEF[fort_type] * (1.5 if legion_statue else 1) + LegionPartsCoef + ExtraInCastleDwellings + external_dwellings ) * (1.5 if grail else 1) + Week


def approx_external_dwelling_growth(level) -> int:
    global BASE_APPROX
    return BASE_APPROX[level]
