from ..town import Town, HeroClass

DATA = []

DATA.append(Town("Castle"))
DATA.append(Town("Rampart"))
DATA.append(Town("Tower"))
DATA.append(Town("Inferno"))
DATA.append(Town("Necropolis"))
DATA.append(Town("Dungeon"))
DATA.append(Town("Stronghold"))
DATA.append(Town("Fortress"))

HEROCLASSES = []

HEROCLASSES.append(HeroClass('Castle', 'Knight', 0))
HEROCLASSES.append(HeroClass('Castle', 'Cleric', 1))
HEROCLASSES.append(HeroClass('Rampart', 'Ranger', 0))
HEROCLASSES.append(HeroClass('Rampart', 'Druid', 1))
HEROCLASSES.append(HeroClass('Tower', 'Alchemist', 0))
HEROCLASSES.append(HeroClass('Tower', 'Wizard', 1))
HEROCLASSES.append(HeroClass('Inferno', 'Demoniac', 0))
HEROCLASSES.append(HeroClass('Inferno', 'Heretic', 1))
HEROCLASSES.append(HeroClass('Necropolis', 'Death Knight', 0))
HEROCLASSES.append(HeroClass('Necropolis', 'Necromancer', 1))
HEROCLASSES.append(HeroClass('Dungeon', 'Overlord', 0))
HEROCLASSES.append(HeroClass('Dungeon', 'Warlock', 1))
HEROCLASSES.append(HeroClass('Stronghold', 'Barbarian', 0))
HEROCLASSES.append(HeroClass('Stronghold', 'Battle Mage', 1))
HEROCLASSES.append(HeroClass('Fortress', 'Beastmaster', 0))
HEROCLASSES.append(HeroClass('Fortress', 'Witch', 1))
