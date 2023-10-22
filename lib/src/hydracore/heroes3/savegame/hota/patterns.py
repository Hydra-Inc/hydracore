import re

# --------------------------------------------------------------------- Hero --

# Main Regex for HOTA Hero described here:
# https://github.com/suurjaak/h3sed/blob/master/src/h3sed/plugins/version/hota.py

# Since savefile format is unknown, hero structs are identified heuristically,
# by matching byte patterns.
HERO_REGEX = re.compile(b"""
    (.{1}\x00{1} | \xFF{2} ) #   2 bytes: x location of the hero               -195..-194
    (.{1}\x00{1} | \xFF{2} ) #   2 bytes: y location of the hero               -193..-192
    (.{1}\x00{1} | \xFF{2} ) #   2 bytes: z location     0 - up, 1 - under     -191..-190

    .{20}                    #  20 bytes: unkown                               -189..-170

    [\xFF\x00-\x07]{1}       #   1 byte: color of the hero                     -169..-169

    .{10}                    #  10 bytes: unkown                               -168..-159

    [\x00-\x20]{1}           #   1 byte: heroclass                             -158..-158

    .{19}                    #  19 bytes: unkown                               -157..-139

    .{4}                     #   4 bytes: movement points in total             -138..-135
    .{4}                     #   4 bytes: movement points remaining            -134..-131
    .{4}                     #   4 bytes: experience                           -130..-127
    [\x00-\x1C][\x00]{3}     #   4 bytes: skill slots used                     -126..-123
    .{2}                     #   2 bytes: spell points remaining               -122..-121
    .{1}                     #   1 byte:  hero level                           -120..-120

    .{63}                    #  63 bytes: unknown                              -119..-57

    .{28}                    #  28 bytes: 7 4-byte creature IDs                -56..-29
    .{28}                    #  28 bytes: 7 4-byte creature counts             -28..-1

                             #  13 bytes: hero name, null-padded               0..12
    (?P<name>[^\x00-\x20,\xF0-\xFF].{12})
    [\x00-\x03]{29}          #  29 bytes: skill levels (Interference last)     13..41
    .{27}                    #  27 bytes: skill slots (legacy, unused)         42..68
    .{4}                     #   4 bytes: primary stats                        69..72

    [\x00-\x01]{70}          #  70 bytes: spells book                          73..142
    [\x00-\x01]{70}          #  70 bytes: spells available                     143..212

                             # 152 bytes: 19 8-byte equipments worn            213..364
                             # Blank spots:   FF FF FF FF 00 00 00 00
                             # Artifacts:     XY 00 00 00 FF FF FF FF
                             # Scrolls:       XY 00 00 00 00 00 00 00
                             # Catapult etc:  XY 00 00 00 XY XY 00 00
                             # Strange spots: FF FF FF FF XY 00 00 00  <-- looks like after moving spell scroll
    ( ((.\x00{3}) | \xFF{4}) (\x00{4} | \xFF{4} | (.{2}\x00{2})) ){19}

                             # 512 bytes: 64 8-byte artifacts in backpack      365..876   THIS IS A BUG!!!
    (?P<arts>( (((.\x00{3}) | \xFF{4}) (.\x00{3} | \xFF{4})) | (\x01\x00{3} (.\x00{3})) ){64})

                             # 10 bytes: slots taken by combination artifacts 877..886
    .[\x00-\x01]{6}[\x00-\x02][\x00-\x01][\x00-\x05]

    .{36}                    #  36 bytes: unknown                             887..922
    [\x00-\x1C]{29}          #  29 bytes: skill slots                         923..951
""", re.VERBOSE | re.DOTALL)

HERO_NAME_OFFSET = 138+57
HERO_REGEX_EXTRA = 0


# Mapping of the fields inside found BLOB using Regex.
# Also taken from the source of h3sed project!

# Index for byte start of various attributes in hero bytearray
HERO_OFFSETS = {
    "x": -195,  # location X coord
    "y": -193,  # location Y coord
    "z": -191,  # location Z coord, 0 - up world, 1 - under world

    "color": -169,  # player color

    "heroclass": -158,  # class of the hero

    "movement_total": -138,  # Movement points in total
    "movement_left": -134,  # Movement points remaining

    "exp": -130,  # Experience points
    "mana": -122,  # Spell points remaining
    "level": -120,  # Hero level

    "skills_count": -126,  # Skills count
    "skills_level":     13,  # Skill levels
    "skills_slot":     923,  # Skill slots    # CHANGED!

    "army_types": -56,  # Creature type IDs
    "army_counts": -28,  # Creature counts

    "name":              0,  # Hero name

    "spells_book":      73,  # Spells in book
    "spells_available": 143,  # All spells available for casting

    "attack":           69,  # Primary attribute: Attack
    "defense":          70,  # Primary attribute: Defense
    "power":            71,  # Primary attribute: Spell Power
    "knowledge":        72,  # Primary attribute: Knowledge

    "helm":             213,  # Helm slot
    "cloak":            221,  # Cloak slot
    "neck":             229,  # Neck slot
    "weapon":           237,  # Weapon slot
    "shield":           245,  # Shield slot
    "armor":            253,  # Armor slot
    "lefthand":         261,  # Left hand slot
    "righthand":        269,  # Right hand slot
    "feet":             277,  # Feet slot
    "side1":            285,  # Side slot 1
    "side2":            293,  # Side slot 2
    "side3":            301,  # Side slot 3
    "side4":            309,  # Side slot 4
    "ballista":         317,  # Ballista slot
    "ammo":             325,  # Ammo Cart slot
    "tent":             333,  # First Aid Tent slot
    "catapult":         341,  # Catapult slot
    "spellbook":        349,  # Spellbook slot
    "side5":            357,  # Side slot 5
    "inventory":        365,  # Inventory start

    "reserved": {            # Slots reserved by combination artifacts
        "helm":        878,
        "cloak":       879,
        "neck":        880,
        "weapon":      881,
        "shield":      882,
        "armor":       883,
        "hand":        884,  # For both left and right hand, \x00-\x02
        "feet":        885,
        "side":        886,  # For all side slots, \x00-\x05
    },

}


HERO_REGEX_ORIG = re.compile(b"""
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
    [\x00-\x03]{29}          #  29 bytes: skill levels (Interference last)     151-179
    .{27}                    #  27 bytes: skill slots (legacy, unused)         180-206
    .{4}                     #   4 bytes: primary stats                        207-210

    [\x00-\x01]{70}          #  70 bytes: spells book                          211-280
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

    .{36}                    #  36 bytes: unknown                             1025-1060
    [\x00-\x1C]{29}          #  29 bytes: skill slots                         1061-1089
""", re.VERBOSE | re.DOTALL)


# Regex to locate the date
DATE_REGEX_OLD = re.compile(b"""
    [\xFF\x01\x04\x40]{10,}    # some stranges '@'

    [\xFF\x01\x04\x40]{32,}    # followed by 0xff
    [\xFF]{160,}               # followed by 0xff
    [^\xFF]                    # usually a null
    .{10}                      # something

    (?P<day>[\x01-\x07])\x00   # 2 bytes - day
    (?P<week>[\x01-\x04])\x00  # 2 bytes - week
    (?P<month>[\x01-\x50])\x00 # 2 bytes - month - max - 50 months!

""", re.VERBOSE | re.DOTALL)

DATE_REGEX = re.compile(b"""
    [\xFF]{160,}               # followed by 0xff
    [^\xFF]                    # usually a null
    .{10}                      # something

    (?P<day>[\x01-\x07])\x00   # 2 bytes - day
    (?P<week>[\x01-\x04])\x00  # 2 bytes - week
    (?P<month>[\x01-\x50])\x00 # 2 bytes - month - max - 50 months!

""", re.VERBOSE | re.DOTALL)



# DATE_REGEX = re.compile(b"""
#    \x40{160,}                 # some stranges '@'
#
#    \xFF{160,}                 # followed by 0xff
#
#    [^\xFF]                    # usually a null
#    .{10}                      # something
#
#    (?P<day>[\x01-\x07])\x00   # 2 bytes - day
#    (?P<week>[\x01-\x04])\x00  # 2 bytes - week
#    (?P<month>[\x01-\x50])\x00 # 2 bytes - month - max - 50 months!
#
# """, re.VERBOSE | re.DOTALL)


# Map file REGEX
MAP_FILE_REGEX = re.compile(b"""
    \x03                       # starts with 0x03
    ([\\[\\]a-zA-Z0-9 \\.\x2E\x3B-]+\\.h3m) # file name
""", re.VERBOSE | re.DOTALL)


# Title and description file REGEX
TITLE_AND_DESCRIPTION_REGEX = re.compile(b"""
    H3SVG.{65}                      # start of the file
    ( (?P<title1>[^\x00\x01]{3,}) | .\x01 (?P<title2>[^\x00\x01]+) ) [\x00-\x01] 
    
    (?P<description>[\\[\\]a-zA-Z0-9 \xC0-\xFF\xB8\xA8\\.\x2c\x2d\x3f;-]+) 
    #\x01\x00
""", re.VERBOSE | re.DOTALL)
