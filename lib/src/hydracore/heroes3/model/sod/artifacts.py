from ..arch import Slot
from ..artifact import Artifact
from ..base.artifacts import DATA as BASE_DATA
from ..spell import Spells


DATA = []

# BASE artifacts
for art in BASE_DATA:
    DATA.append(art)

# SOD artifacts
DATA.append(Artifact.Combination("Admiral's Hat", [Slot.helm, Slot.neck], None, ["Scuttle Boat", "Summon Boat"]))
DATA.append(Artifact.Combination("Angelic Alliance", [Slot.weapon, Slot.helm, Slot.neck, Slot.armor, Slot.shield, Slot.feet], [21, 21, 21, 21]))
DATA.append(Artifact.Relic("Armageddon's Blade", Slot.weapon, [+3, +3, +3, +6], ["Armageddon"]))
DATA.append(Artifact.Combination("Armor of the Damned", [Slot.armor, Slot.helm, Slot.weapon, Slot.shield], [+3, +3, +2, +2]))
DATA.append(Artifact.Combination("Bow of the Sharpshooter", [Slot.side, Slot.side, Slot.side]))
DATA.append(Artifact.Combination("Cloak of the Undead King", [Slot.cloak, Slot.neck, Slot.feet]))
DATA.append(Artifact.Combination("Cornucopia", [Slot.side, Slot.hand, Slot.hand, Slot.cloak]))
DATA.append(Artifact.Combination("Elixir of Life", [Slot.side, Slot.hand, Slot.hand]))
DATA.append(Artifact.Combination("Power of the Dragon Father", [Slot.armor, Slot.helm, Slot.neck, Slot.weapon, Slot.shield, Slot.hand, Slot.hand, Slot.cloak, Slot.feet], [16, 16, 16, 16]))
DATA.append(Artifact.Combination("Ring of the Magi", [Slot.hand, Slot.neck, Slot.cloak]))
DATA.append(Artifact.Combination("Statue of Legion", [Slot.side, Slot.side, Slot.side, Slot.side, Slot.side]))
DATA.append(Artifact.Combination("Titan's Thunder", [Slot.weapon, Slot.helm, Slot.armor, Slot.shield], [+9, +9, +8, +8], ["Titan's Lightning Bolt"]))
DATA.append(Artifact.Relic("Vial of Dragonblood", Slot.side))
DATA.append(Artifact.Combination("Wizard's Well", [Slot.side, Slot.side, Slot.side]))

# SCROLLS
for spell in Spells('sod').All():
    DATA.append(Artifact.Scroll(spell.name))

