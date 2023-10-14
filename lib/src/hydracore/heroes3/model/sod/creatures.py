from ..creature import Creature
from ..base.creatures import DATA as BASE_DATA


DATA = []

# BASE creatures
for cre in BASE_DATA:
    DATA.append(cre)


# SOD creatures

# ------------------------------------------------------------------ Conflux --
 
DATA.append(Creature.Conflux(1, 0, "Pixie", 55))
DATA.append(Creature.Conflux(1, 1, "Sprite", 95))
DATA.append(Creature.Conflux(2, 0, "Air Elemental", 356))
DATA.append(Creature.Conflux(2, 1, "Storm Elemental", 486))
DATA.append(Creature.Conflux(3, 0, "Water Elemental", 315))
DATA.append(Creature.Conflux(3, 1, "Ice Elemental", 380))
DATA.append(Creature.Conflux(4, 0, "Fire Elemental", 345))
DATA.append(Creature.Conflux(4, 1, "Energy Elemental", 470))
DATA.append(Creature.Conflux(5, 0, "Earth Elemental", 330))
DATA.append(Creature.Conflux(5, 1, "Magma Elemental", 490))
DATA.append(Creature.Conflux(6, 0, "Psychic Elemental", 1669))
DATA.append(Creature.Conflux(6, 1, "Magic Elemental", 2012))
DATA.append(Creature.Conflux(7, 0, "Firebird", 4336))
DATA.append(Creature.Conflux(7, 1, "Phoenix", 6721))

# ------------------------------------------------------------------ Neutral --

DATA.append(Creature.Neutral(8, 0, "Azure Dragon", 78845))
DATA.append(Creature.Neutral(2, 0, "Boar", 145))
DATA.append(Creature.Neutral(8, 0, "Crystal Dragon", 39338))
DATA.append(Creature.Neutral(6, 0, "Enchanter", 1210))
DATA.append(Creature.Neutral(8, 0, "Faerie Dragon", 30501))
DATA.append(Creature.Neutral(1, 0, "Halfling", 75))
DATA.append(Creature.Neutral(3, 0, "Mummy", 270))
DATA.append(Creature.Neutral(3, 0, "Nomad", 345))
DATA.append(Creature.Neutral(1, 0, "Peasant", 10))
DATA.append(Creature.Neutral(2, 0, "Rogue", 135))
DATA.append(Creature.Neutral(8, 0, "Rust Dragon", 26433))
DATA.append(Creature.Neutral(4, 0, "Sharpshooter", 585))
DATA.append(Creature.Neutral(5, 0, "Troll", 1024))

