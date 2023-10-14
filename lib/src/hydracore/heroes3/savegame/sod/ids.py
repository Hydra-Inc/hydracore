from ..base.ids import IDs as BASE_IDS


# From: https://github.com/suurjaak/h3sed/blob/master/src/h3sed/plugins/version/sod.py


"""IDs of artifacts, creatures and spells in savefile."""
IDs = {
    # Artifacts
    "Admiral's Hat":                     0x88,
    "Angelic Alliance":                  0x81,
    "Armageddon's Blade":                0x80,
    "Armor of the Damned":               0x84,
    "Bow of the Sharpshooter":           0x89,
    "Cloak of the Undead King":          0x82,
    "Cornucopia":                        0x8C,
    "Elixir of Life":                    0x83,
    "Power of the Dragon Father":        0x86,
    "Ring of the Magi":                  0x8B,
    "Statue of Legion":                  0x85,
    "Titan's Thunder":                   0x87,
    "Vial of Dragonblood":               0x7F,
    "Wizard's Well":                     0x8A,

    # Creatures
    "Azure Dragon":                      0x84,
    "Boar":                              0x8C,
    "Crystal Dragon":                    0x85,
    "Diamond Golem":                     0x75,
    "Enchanter":                         0x88,
    "Energy Elemental":                  0x81,
    "Faerie Dragon":                     0x86,
    "Firebird":                          0x82,
    "Gold Golem":                        0x74,
    "Halfling":                          0x8A,
    "Ice Elemental":                     0x7B,
    "Magic Elemental":                   0x79,
    "Magma Elemental":                   0x7D,
    "Mummy":                             0x8D,
    "Nomad":                             0x8E,
    "Peasant":                           0x8B,
    "Phoenix":                           0x83,
    "Pixie":                             0x76,
    "Psychic Elemental":                 0x78,
    "Rogue":                             0x8F,
    "Rust Dragon":                       0x87,
    "Sharpshooter":                      0x89,
    "Sprite":                            0x77,
    "Storm Elemental":                   0x7F,
    "Troll":                             0x90,

    # Spells
    "Titan's Lightning Bolt":            0x39,
}

XID = BASE_IDS
XID.update(IDs)
IDs = XID

