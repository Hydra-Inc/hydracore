from ..creature import Creature
from ..hota.creatures import DATA as BASE_DATA


DATA = []

# SOD creatures
for cre in BASE_DATA:
    DATA.append(cre)


# HOTA 1.7 creatures


# --------------------------------------------------------------------- Cove --

DATA.append(Creature.Factory(1, 0, "Halfling", 0))
DATA.append(Creature.Factory(1, 1, "Halfling Grenadier", 0))
DATA.append(Creature.Factory(2, 0, "Mechanic", 0))
DATA.append(Creature.Factory(2, 1, "Engineer", 0))
DATA.append(Creature.Factory(3, 0, "Armadillo", 0))
DATA.append(Creature.Factory(3, 1, "Bellwether Armadillo", 0))
DATA.append(Creature.Factory(4, 0, "Automaton", 0))
DATA.append(Creature.Factory(4, 1, "Sentinel Automaton", 0))
DATA.append(Creature.Factory(5, 0, "Sandworm", 0))
DATA.append(Creature.Factory(5, 1, "Olgoi-Khorkhoi", 0))
DATA.append(Creature.Factory(6, 0, "Gunslinger", 0))
DATA.append(Creature.Factory(6, 1, "Bounty Hunter", 0))
DATA.append(Creature.Factory(7, 0, "Couatl", 0))
DATA.append(Creature.Factory(7, 1, "Crimson Couatl", 0))
DATA.append(Creature.Factory(7, 0, "Dreadnought", 0))
DATA.append(Creature.Factory(7, 1, "Juggernaut", 0))



# ------------------------------------------------------------------ Neutral --
