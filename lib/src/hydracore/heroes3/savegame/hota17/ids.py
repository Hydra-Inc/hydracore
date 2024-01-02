from ..hota.ids import IDs as BASE_IDS

# From: https://github.com/suurjaak/h3sed/blob/master/src/h3sed/plugins/version/hota.py

"""IDs of all items in savefile."""
IDs = {
    # Artifacts
    
    # Creatures
    # "Halfling":                          0xAA,
    "Halfling Grenadier":                0xAB,
    "Mechanic":                          0xAC,
    "Engineer":                          0xAD,

    "Armadillo":                         0xAE,
    "Bellwether Armadillo":              0xAF,

    "Automaton":                         0xB0,
    "Sentinel Automaton":                0xB1,

    "Sandworm":                          0xB2,
    "Olgoi-Khorkhoi":                    0xB3,

    "Gunslinger":                        0xB4,
    "Bounty Hunter":                     0xB5,

    "Couatl":                            0xB6,
    "Crimson Couatl":                    0xB7,
    "Dreadnought":                       0xB8,
    "Juggernaut":                        0xB9,

    # Skills
    
    # Spells
    
    # Hero classes
    "Mercenary":                         0x14,
    "Artificer":                         0x15,

}

XID = BASE_IDS
XID.update(IDs)
IDs = XID
