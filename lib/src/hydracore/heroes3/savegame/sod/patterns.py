import re




# --------------------------------------------------------------------- Hero --

# Main Regex for SOD Hero described here:
# https://github.com/suurjaak/h3sed/blob/master/src/h3sed/plugins/hero/__init__.py

# Since savefile format is unknown, hero structs are identified heuristically,
# by matching byte patterns.
HERO_REGEX = re.compile(b"""
    # There are at least 60 bytes more at front, but those can also include
    # hero biography, making length indeterminate.
    # Bio ends at position -32 from total movement point start.
    # If bio end position is \x00, then bio is empty, otherwise bio extends back
    # until a 4-byte span giving bio length (which always ends with \x00
    # because bio can't be gigabytes long).

    .{4}                     #   4 bytes: movement points in total             000-003
    .{4}                     #   4 bytes: movement points remaining            004-007
    .{4}                     #   4 bytes: experience                           008-011
    [\x00-\x1C][\x00]{3}     #   4 bytes: skill slots used                     012-015
    .{2}                     #   2 bytes: spell points remaining               016-017
    .{1}                     #   1 byte:  hero level                           018-018

    .{63}                    #  63 bytes: unknown                              019-081

    .{28}                    #  28 bytes: 7 4-byte creature IDs                082-109
    .{28}                    #  28 bytes: 7 4-byte creature counts             110-137

                             #  13 bytes: hero name, null-padded               138-150
    (?P<name>[^\x00-\x20,\xF0-\xFF].{12})
    [\x00-\x03]{28}          #  28 bytes: skill levels                         151-178
    [\x00-\x1C]{28}          #  28 bytes: skill slots                          179-206
    .{4}                     #   4 bytes: primary stats                        207-210

    [\x00-\x01]{70}          #  70 bytes: spells in book                       211-280
    [\x00-\x01]{70}          #  70 bytes: spells available                     281-350

                             # 152 bytes: 19 8-byte equipments worn            351-502
                             # Blank spots:   FF FF FF FF 00 00 00 00
                             # Artifacts:     XY 00 00 00 FF FF FF FF
                             # Scrolls:       XY 00 00 00 00 00 00 00
                             # Catapult etc:  XY 00 00 00 XY XY 00 00
    ( ((.\x00{3}) | \xFF{4}) (\x00{4} | \xFF{4} | (.{2}\x00{2})) ){19}

                             # 512 bytes: 64 8-byte artifacts in backpack      503-1014
    ( ((.\x00{3}) | \xFF{4}) (\x00{4} | \xFF{4}) ){64}

                             # 10 bytes: slots taken by combination artifacts 1015-1024
    .[\x00-\x01]{6}[\x00-\x02][\x00-\x01][\x00-\x05]
""", re.VERBOSE | re.DOTALL)

HERO_NAME_OFFSET = 138
HERO_REGEX_EXTRA = 0


# Mapping of the fields inside found BLOB using Regex.
# Also taken from the source of h3sed project!

# Index for byte start of various attributes in hero bytearray
HERO_OFFSETS = {
    "movement_total":     -138, # Movement points in total
    "movement_left":      -134, # Movement points remaining

    "exp":                -130, # Experience points
    "mana":              -122, # Spell points remaining
    "level":             -120, # Hero level

    "skills_count":      -126, # Skills count
    "skills_level":     13, # Skill levels
    "skills_slot":      41, # Skill slots

    "army_types":        -56, # Creature type IDs
    "army_counts":      -28, # Creature counts

    "spells_book":      73, # Spells in book
    "spells_available": 143, # All spells available for casting

    "attack":           69, # Primary attribute: Attack
    "defense":          70, # Primary attribute: Defense
    "power":            71, # Primary attribute: Spell Power
    "knowledge":        72, # Primary attribute: Knowledge

    "helm":             213, # Helm slot
    "cloak":            221, # Cloak slot
    "neck":             229, # Neck slot
    "weapon":           237, # Weapon slot
    "shield":           245, # Shield slot
    "armor":            253, # Armor slot
    "lefthand":         261, # Left hand slot
    "righthand":        269, # Right hand slot
    "feet":             277, # Feet slot
    "side1":            285, # Side slot 1
    "side2":            293, # Side slot 2
    "side3":            301, # Side slot 3
    "side4":            309, # Side slot 4
    "ballista":         317, # Ballista slot
    "ammo":             325, # Ammo Cart slot
    "tent":             333, # First Aid Tent slot
    "catapult":         341, # Catapult slot
    "spellbook":        349, # Spellbook slot
    "side5":            357, # Side slot 5
    "inventory":        365, # Inventory start

    "reserved": {            # Slots reserved by combination artifacts
        "helm":        878,
        "cloak":       879,
        "neck":        880,
        "weapon":      881,
        "shield":      882,
        "armor":       883,
        "hand":        884, # For both left and right hand, \x00-\x02
        "feet":        885,
        "side":        886, # For all side slots, \x00-\x05
    },

}


