from ..base.ids import IDs as BASE_IDS

# From: https://github.com/suurjaak/h3sed/blob/master/src/h3sed/plugins/version/hota.py

"""IDs of all items in savefile."""
IDs = {
    # Artifacts
    "Admiral's Hat":                     0x88,
    "Angelic Alliance":                  0x81,
    "Armageddon's Blade":                0x80,
    "Armor of the Damned":               0x84,
    "Bow of the Sharpshooter":           0x89,
    "Cape of Silence":                   0x9F,
    "Charm of Eclipse":                  0xA2,
    "Cloak of the Undead King":          0x82,
    "Cornucopia":                        0x8C,
    "Crown of the Five Seas":            0x96,
    "Demon's Horseshoe":                 0x99,
    "Diplomat's Cloak":                  0x8D,
    "Elixir of Life":                    0x83,
    "Golden Goose":                      0xA0,
    "Hideous Mask":                      0x9B,
    "Horn of the Abyss":                 0xA1,
    "Ironfist of the Ogre":              0x8F,
    "Pendant of Downfall":               0x9D,
    "Pendant of Reflection":             0x8E,
    "Plate of Dying Light":              0xA4,
    "Power of the Dragon Father":        0x86,
    "Ring of Oblivion":                  0x9E,
    "Ring of Suppression":               0x9C,
    "Ring of the Magi":                  0x8B,
    "Royal Armor of Nix":                0x95,
    "Runes of Imminency":                0x98,
    "Seal of Sunset":                    0xA3,
    "Shaman's Puppet":                   0x9A,
    "Shield of Naval Glory":             0x94,
    "Statue of Legion":                  0x85,
    "Titan's Thunder":                   0x87,
    "Trident of Dominion":               0x93,
    "Vial of Dragonblood":               0x7F,
    "Wayfarer's Boots":                  0x97,
    "Wizard's Well":                     0x8A,

    # Special artifacts
    "Cannon":                            0x92,

    # Creatures
    "Ayssid":                            0xA0,
    "Azure Dragon":                      0x84,
    "Boar":                              0x8C,
    "Corsair":                           0x9E,
    "Crew Mate":                         0x9B,
    "Crystal Dragon":                    0x85,
    "Diamond Golem":                     0x75,
    "Enchanter":                         0x88,
    "Energy Elemental":                  0x81,
    "Faerie Dragon":                     0x86,
    "Fangarm":                           0xA8,
    "Firebird":                          0x82,
    "Gold Golem":                        0x74,
    "Halfling":                          0x8A,
    "Haspid":                            0xA6,
    "Ice Elemental":                     0x7B,
    "Leprechaun":                        0xA9,
    "Magic Elemental":                   0x79,
    "Magma Elemental":                   0x7D,
    "Mummy":                             0x8D,
    "Nix Warrior":                       0xA4,
    "Nix":                               0xA3,
    "Nomad":                             0x8E,
    "Nymph":                             0x99,
    "Oceanid":                           0x9A,
    "Peasant":                           0x8B,
    "Phoenix":                           0x83,
    "Pirate":                            0x9D,
    "Pixie":                             0x76,
    "Psychic Elemental":                 0x78,
    "Rogue":                             0x8F,
    "Rust Dragon":                       0x87,
    "Satyr":                             0xA7,
    "Sea Dog":                           0x97,
    "Sea Serpent":                       0xA5,
    "Sea Witch":                         0xA1,
    "Seaman":                            0x9C,
    "Sharpshooter":                      0x89,
    "Sorceress":                         0xA2,
    "Sprite":                            0x77,
    "Steel Golem":                       0xAA,
    "Storm Elemental":                   0x7F,
    "Stormbird":                         0x9F,
    "Troll":                             0x90,

    # Skills
    "Interference":                      0x1C,

    # Spells
    "Titan's Lightning Bolt":            0x39,

    # Hero classes
    "Captain":                           0x12,
    "Navigator":                         0x13,

}

XID = BASE_IDS
XID.update(IDs)
IDs = XID
