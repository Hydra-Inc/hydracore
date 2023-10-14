from ..arch import Slot
from ..artifact import Artifact
from ..base.artifacts import DATA as BASE_DATA
from ..spell import Spells


DATA = []

for art in BASE_DATA:
    DATA.append(art)

# HOTA artifacts
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

DATA.append(Artifact.Major("Cape of Silence", Slot.cloak))
DATA.append(Artifact.Minor("Charm of Eclipse", Slot.side))
DATA.append(Artifact.Major("Crown of the Five Seas", Slot.helm, [0,  0,  0, +6]))
DATA.append(Artifact.Treasure("Demon's Horseshoe", Slot.side))
DATA.append(Artifact.Combination("Diplomat's Cloak", [Slot.cloak, Slot.neck, Slot.hand]))
DATA.append(Artifact.Combination("Golden Goose", [Slot.side, Slot.side, Slot.side]))
DATA.append(Artifact.Minor("Hideous Mask", Slot.side))
DATA.append(Artifact.Relic("Horn of the Abyss", Slot.side))
DATA.append(Artifact.Combination("Ironfist of the Ogre", [Slot.weapon, Slot.helm, Slot.armor, Slot.shield], [+5, +5, +4, +4]))
DATA.append(Artifact.Major("Pendant of Downfall", Slot.neck))
DATA.append(Artifact.Combination("Pendant of Reflection", [Slot.neck, Slot.feet, Slot.cloak]))
DATA.append(Artifact.Relic("Plate of Dying Light", Slot.armor))
DATA.append(Artifact.Major("Ring of Oblivion", Slot.hand))
DATA.append(Artifact.Treasure("Ring of Suppression", Slot.hand))
DATA.append(Artifact.Major("Royal Armor of Nix", Slot.armor, [0,  0, +6,  0]))
DATA.append(Artifact.Treasure("Runes of Imminency", Slot.side))
DATA.append(Artifact.Minor("Seal of Sunset", Slot.hand))
DATA.append(Artifact.Minor("Shaman's Puppet", Slot.side))
DATA.append(Artifact.Major("Shield of Naval Glory", Slot.shield, [0, +7,  0,  0]))
DATA.append(Artifact.Major("Trident of Dominion", Slot.weapon, [+7,  0,  0,  0]))
DATA.append(Artifact.Major("Wayfarer's Boots", Slot.feet))


# SCROLLS
for spell in Spells('hota').All():
    DATA.append(Artifact.Scroll(spell.name))
