HydraCore Library
=================

A free Python library offers useful tools for manipulating the popular game "Heroes of Might and Magic III" by 3DO.

The initial goal of this library was to create a program that could help train users in playing PvP games on the Jebus Outcast/Jebus Cross templates without actually needing a human opponent. The idea is to enhance the computer opponent by modifying a late-game save file, which you can then load and battle against a formidable computer adversary.

The save game format of the original game was unknown, but enthusiasts from all over the world (see the 'Thanks to' section) have reverse-engineered it. Now, we can develop handy tools like this one.


Command line interface
======================


Usage of Heroes 3 model viewer
------------------------------

Allows to list internal structure of SoD (Shadow of Death) and HotA (Hprn of the Abyss) game versions.

List all HotA artifacts:
```bash
./hydracore heroes3 model hota artifacts
```
List all HotA creatures:
```bash
./hydracore heroes3 model hota creatures
```
List all HotA skills:
```bash
./hydracore heroes3 model hota skills
```
List all HotA spells:
```bash
./hydracore heroes3 model hota spells
```
List all HotA towns:
```bash
./hydracore heroes3 model hota towns
```
List all HotA heroclasses:
```bash
./hydracore heroes3 model hota heroclasses
```
List all HotA heroes:
```bash
./hydracore heroes3 model hota hero
```
List all HotA heroes:
```bash
./hydracore heroes3 model hota templates
```

Usage of SaveGame viewer and changer
------------------------------------

Utility to play with the save game file, allows to debug and easy test our file for different infromation.

Print full game info from the given file.
```bash
./hydracore heroes3 savegame data/heroes3/savegames/testing/x5.GM1 print gameinfo
```

Print all heroes from the provided savegame file:
```bash
./hydracore heroes3 savegame data/heroes3/savegames/testing/x5.GM1 print heroes
```

Dump raw unpacked heroes data from save game:
```bash
./hydracore heroes3 savegame data/heroes3/savegames/testing/x5.GM1 dump hero --out-file aa.bin --filter-name Манфред
```

Change hero:
*currently not done yet*

You may see more in the help of the command line utility.


Python API
======================

To be continued.

List all HotA relict artifacts:
```python
from hydracore.heroes3.model.artifact import Artifacts

for artifact in Artifacts('hota').Relic():
    print(artifact.name)
```



Thanks to
---------

h3sed a Heroes3 Savegame Editor by Erki Suurjaak: https://github.com/suurjaak/h3sed

Lot's of useful data here (Heroes Community forum): http://heroescommunity.com/viewthread.php3?TID=18817

Thanks to the marvelous authors of our beloved game: Heroes of Might and Magic III, (c) 1999 3DO.

This software is not an official addon or a set of official utilities for Heroes 3. Actually Heroes, Might and Magic, Heroes of Might and Magic, Ubisoft and the Ubisoft logo are trademarks of Ubisoft Entertainment in the U.S. and/or other countries.


License
-------

Copyright (c) 2023 by hydra-core aka TechnoCore

Released as free open source software under the MIT License,
see [LICENSE](LICENSE) for full license text.
