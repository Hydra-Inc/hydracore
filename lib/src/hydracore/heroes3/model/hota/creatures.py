from ..creature import Creature
from ..sod.creatures import DATA as BASE_DATA


DATA = []

# SOD creatures
for cre in BASE_DATA:
    DATA.append(cre)


# HOTA creatures


# --------------------------------------------------------------------- Cove --

DATA.append(Creature.Cove(1, 0, "Nymph", 57))
DATA.append(Creature.Cove(1, 1, "Oceanid", 75))
DATA.append(Creature.Cove(2, 0, "Crew Mate", 155))
DATA.append(Creature.Cove(2, 1, "Seaman", 174))
DATA.append(Creature.Cove(3, 0, "Pirate", 312))
DATA.append(Creature.Cove(3, 1, "Corsair", 407))
DATA.append(Creature.Cove(3, 2, "Sea Dog", 602))
DATA.append(Creature.Cove(4, 0, "Stormbird", 502))
DATA.append(Creature.Cove(4, 1, "Ayssid", 645))
DATA.append(Creature.Cove(5, 0, "Sea Witch", 790))
DATA.append(Creature.Cove(5, 1, "Sorceress", 852))
DATA.append(Creature.Cove(6, 0, "Nix", 1415))
DATA.append(Creature.Cove(6, 1, "Nix Warrior", 2116))
DATA.append(Creature.Cove(7, 0, "Sea Serpent", 3953))
DATA.append(Creature.Cove(7, 1, "Haspid", 7220))

# ------------------------------------------------------------------ Neutral --

DATA.append(Creature.Neutral(2, 0, "Leprechaun", 208))
DATA.append(Creature.Neutral(5, 0, "Fangarm", 929))
DATA.append(Creature.Neutral(4, 0, "Satyr", 518))
DATA.append(Creature.Neutral(4, 0, "Steel Golem", 597))
