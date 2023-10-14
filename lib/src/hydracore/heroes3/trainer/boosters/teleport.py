from typing import List

from hydracore.heroes3.model.hero import Hero

from ..booster import Booster


class TeleportBooster(Booster):
    pass


class TeleportNearOther(TeleportBooster):

    def boost(self, teleport_heroes: List[Hero], other: Hero):

        if self.Trainer.MapTerrainInfo is None:
            raise RuntimeError(
                'Terrain info is not supplied to perform accurate teleport')

        if other is None:
            raise RuntimeError(
                'Player main hero not identified, cant teleport')

        #
        # Order of checking nearest empty slots:
        #
        #     4 5 6
        #     3 H 7
        #     2 1 8
        #

        locations = [
            [0,  1],
            [-1,  1],
            [-1,  0],
            [-1, -1],
            [0, -1],
            [1, -1],
            [1,  0],
            [1,  1]
        ]

        if self.Trainer.verbose:
            print(f'Other hero located at: {other.X} {other.Y} {other.Z}')

        for the_hero in teleport_heroes:
            if self.Trainer.verbose:
                print(f'Teleporting {the_hero.Name}')

            already = False
            for loc in locations:
                X = other.X + loc[0]
                Y = other.Y + loc[1]
                Z = other.Z

                is_empty = self.Trainer.MapTerrainInfo.is_empty(X, Y, Z)

                if is_empty:
                    for hero in self.Trainer.Heroes:
                        if X == hero.X and Y == hero.Y and Z == hero.Z:
                            if hero.Name == the_hero.Name:
                                already = True
                            else:
                                is_empty = False
                            break

                if already:
                    break

                if is_empty:
                    the_hero.X = X
                    the_hero.Y = Y
                    the_hero.Z = Z

                    if self.Trainer.verbose:
                        print(
                            f'Hero {the_hero.Name} teleported to {X}, {Y}, {Z}')

                    break


class TeleportCenter(TeleportBooster):

    def boost(self, teleport_heroes: List[Hero]):

        if self.Trainer.MapTerrainInfo is None:
            raise RuntimeError(
                'Terrain info is not supplied to perform accurate teleport')

        if self.Trainer.MapTerrainInfo.Size is None:
            raise RuntimeError(
                'Terrain info is not supplied to perform center teleport')

        #
        # Order of checking nearest empty slots:
        #
        #
        #       C
        #     2 1 3
        #     4 5 6
        #

        locations = [
            [0,  1],
            [-1,  1],
            [1,  1],
            [0,  2],
            [1,  2],
        ]

        center = self.Trainer.MapTerrainInfo.Size // 2 + 1

        for the_hero in teleport_heroes:
            if self.Trainer.verbose:
                print(f'Teleporting {the_hero.Name}')

            already = False
            for loc in locations:
                X = center + loc[0]
                Y = center + loc[1]
                Z = 0

                is_empty = self.Trainer.MapTerrainInfo.is_empty(X, Y, Z)

                if is_empty:
                    for hero in self.Trainer.Heroes:
                        if X == hero.X and Y == hero.Y and Z == hero.Z:
                            if hero.Name == the_hero.Name:
                                already = True
                            else:
                                is_empty = False
                            break

                if already:
                    break

                if is_empty:
                    the_hero.X = X
                    the_hero.Y = Y
                    the_hero.Z = Z

                    if self.Trainer.verbose:
                        print(
                            f'Hero {the_hero.Name} teleported to {X}, {Y}, {Z}')

                    break
