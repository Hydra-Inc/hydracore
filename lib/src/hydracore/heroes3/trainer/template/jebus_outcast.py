import copy
import math

from typing import List, Optional

from ..base import TheTemplateTrainer, Difficulty
from ..boosters.hero import HeroBooster, HeroBaseBooster
from ..boosters.teleport import TeleportNearOther, TeleportCenter

from hydracore.heroes3.model.arch import Color
from hydracore.heroes3.model.creature import Creatures, Level, Upgraded
from hydracore.heroes3.model.hero import Hero, MostExperiencedHero, FilterByColor, PlayersColors
from hydracore.heroes3.model.population import FortType, approx_population_grow_per_week_in_town, approx_external_dwelling_growth
from hydracore.heroes3.model.time import Date, days_passed, weeks_passed


# -------------------------------------------------------------- AI Boosters --


def approx_pandoras_army_by_level(level: int) -> int:
    if level == 7:
        return 5
    if level == 6:
        return 10
    if level == 5:
        return 15
    if level == 4:
        return 20
    if level == 3:
        return 30
    if level == 2:
        return 50
    if level == 1:
        return 100
    return 0


class JO_AIHeroArmyBooster(HeroBaseBooster):
    def boost(self, hero: Hero):

        weeks = weeks_passed(self.Trainer.Date)
        self.Creatures = list(Creatures(hero.ver).Town(hero.Town))
        self.TheDate = self.Trainer.Date

        if weeks == 0:
            # this is intial boost, lets issue the date is in future
            if self.Trainer.Difficulty == Difficulty.Easy:
                self.TheDate = Date(1, 2, 1)
            if self.Trainer.Difficulty == Difficulty.Medium:
                self.TheDate = Date(1, 3, 1)
            if self.Trainer.Difficulty == Difficulty.Hard:
                self.TheDate = Date(1, 4, 1)
            if self.Trainer.Difficulty == Difficulty.Impossible:
                self.TheDate = Date(2, 1, 1)

        else:
            # this is not an initial boost
            pass

        # available flows, currently - how much main stacks
        super_variants = {
            'stack_count': {
                'freq': 100,
                'data': {
                    1: 10,
                    2: 6,
                    3: 7,
                    4: 3,
                }
            },
            'demonology': {
                'freq': 0,
            },
            'vampires': {
                'freq': 0,
            },
            'skeletons': {
                'freq': 0,
            }
        }

        variants = {
            5: 10,   # as they are in Pandoras, higher probability
            6: 7,    # ouch! if e.g. Manticoras
            7: 7,    # some one can do this too
            4: 3,    # this is a rare variant but still possible
        }

        if hero.Town == 'Castle':
            variants[5] = 3
            variants[4] = 7
        if hero.Town == 'Rampart':
            variants[5] = 9
            variants[3] = 4
        if hero.Town == 'Tower':
            variants[5] = 6
        if hero.Town == 'Inferno':

            super_variants['demonology']['freq'] = 30
            variants[4] = 2

            variants[5] = 12
        if hero.Town == 'Necropolis':
            super_variants['skeletons']['freq'] = 25

            super_variants['vampires']['freq'] = 30
            variants[4] = 2

            variants[5] = 3

        if hero.Town == 'Dungeon':
            variants[5] = 12
            variants[6] = 3
        if hero.Town == 'Stronghold':
            variants[6] = 4
            variants[7] = 11
        if hero.Town == 'Fortress':
            variants[5] = 12
            variants[6] = 5
        if hero.Town == 'Cove':
            variants[5] = 3
            variants[6] = 12

        # lets start
        hero.DropAllCreatures()

        boosted_stacks = []
        boost_minors = False

        # Select SUPER variant
        super_var_selection = {}
        for super_var, info in super_variants.items():
            super_var_selection[super_var] = info['freq']
        super_variant = self.Trainer.Random.weighted_choice(
            super_var_selection)

        if super_variant == 'stack_count':

            how_much_main_stacks_selection = super_variants[super_variant]['data']
            how_much_main_stacks = self.Trainer.Random.weighted_choice(
                how_much_main_stacks_selection)

            if self.Trainer.verbose:
                print(
                    f'Hero {hero.Name} to be boosted with {how_much_main_stacks} main stacks')

            if how_much_main_stacks <= 2:
                boost_minors = True

            left_variants = copy.deepcopy(variants)

            # add stacks for the hero
            for _ in range(how_much_main_stacks):
                variant = self.Trainer.Random.weighted_choice(left_variants)
                left_variants[variant] = 0

                boosted_stacks.append(variant)

                method = f'boost_level{variant}'
                if not getattr(self.__class__, method):
                    raise RuntimeError(
                        f'Jebus Outcast boost variant level{variant} not implemented')

                # Add stack to hero
                getattr(self.__class__, method)(self, hero)

                if self.Trainer.verbose:
                    print(f'Hero {hero.Name} boosted with tech level{variant}')

        if super_variant == 'demonology':
            boost_minors = True
            self.boost_stack(hero, 4, 2.0)
            boosted_stacks.append(4)

        if super_variant == 'skeletons':
            boost_minors = True
            self.boost_stack(hero, 1, 3.0)
            boosted_stacks.append(1)

        if super_variant == 'vampires':
            boost_minors = True
            self.boost_stack(hero, 4, 1.5)
            boosted_stacks.append(4)

        # Add Dracogeddon, Efreetiegeddon, ...

        # add some minors stacks of 5,6,7 levels, just 1-2-3 count
        if boost_minors:
            left = set(boosted_stacks) - set([5,6,7])
            for stack in left:
                if hero.FreeArmySlot is None:
                    break
                self.boost_stack(hero, stack, 0.2)

        # Random boxes
        self.boost_other_boxes(hero)

        # Refugee any?!
        self.boost_other_stuff(hero)

    def boost_other_boxes(self, hero: Hero):
        pass

    def boost_other_stuff(self, hero: Hero):

        slot = hero.FreeArmySlot()
        if not slot:
            return

        # Refugee stuff
        total = len(self.Creatures)
        allowed = ["Phoenix", "Haspid", "Archangel", "Gold Dragon", "Titan", "Arch Devil", "Black Dragon", "Ancient Behemoth", "Master Genie"]
        select_from = [crid for crid in allowed if Creatures(hero.ver).Get(crid).town != hero.Town]
        ch = self.Trainer.Random.int(0, total)
        if ch < len(select_from):
            hero.AddCreature(slot, select_from[ch], (8-Creatures(hero.ver).Get(select_from[ch]).level))


    def boost_level1(self, hero: Hero):
        return self.boost_stack(hero, 1)

    def boost_level2(self, hero: Hero):
        return self.boost_stack(hero, 2)

    def boost_level3(self, hero: Hero):
        return self.boost_stack(hero, 3)

    def boost_level4(self, hero: Hero):
        return self.boost_stack(hero, 4)

    def boost_level5(self, hero: Hero):
        return self.boost_stack(hero, 5)

    def boost_level6(self, hero: Hero):
        return self.boost_stack(hero, 6)

    def boost_level7(self, hero: Hero):
        return self.boost_stack(hero, 7)

    def boost_stack(self, hero: Hero, level: int, coef: float = 1.0):
        exp = list(Upgraded(Level(self.Creatures, level)))
        if len(exp) == 0:
            raise RuntimeError(
                f"Cant identify upgraded creature for {hero.Town} of level {level}")
        creature = exp[0]

        slot = hero.FreeArmySlot()
        if not slot:
            return

        amount = 0

        weeks = weeks_passed(self.TheDate) + 1

        ext_dwellings = 0
        towns = [None, None]
        towns[0] = {'fort': FortType.Fort, 'built': level <= 2}
        towns[1] = {'fort': FortType.Fort, 'built': level <= 2}

        week = 1
        if week == 1 and week <= weeks:

            # Compute on week growth
            for town in towns:
                if town['built']:
                    amount += approx_population_grow_per_week_in_town(
                        level, town['fort'], ext_dwellings, grail=False, legion_statue=False)

            if self.Trainer.Difficulty == Difficulty.Easy:
                ext_dwellings += self.Trainer.Random.int(0, 2)

                if self.Trainer.Random.int(0, 2) == 0:
                    towns[0]['fort'] = FortType.Citadel
                towns[0]['built'] = True if self.Trainer.Random.int(
                    0, 2) == 0 else False

            if self.Trainer.Difficulty == Difficulty.Medium:
                ext_dwellings += self.Trainer.Random.int(1, 2)

                if self.Trainer.Random.int(0, 1) == 0:
                    towns[0]['fort'] = FortType.Citadel
                towns[0]['built'] = True if self.Trainer.Random.int(
                    0, 1) == 0 else False

            if self.Trainer.Difficulty == Difficulty.Hard:
                ext_dwellings += self.Trainer.Random.int(2, 3)

                towns[0]['fort'] = FortType.Citadel
                towns[0]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Impossible:
                ext_dwellings += self.Trainer.Random.int(3, 5)

                towns[0]['fort'] = FortType.Castle
                towns[0]['built'] = True

            # Take into account extenral swellings
            amount += approx_external_dwelling_growth(level) * ext_dwellings

        week += 1

        if week == 2 and week <= weeks:

            # Compute on week growth
            for town in towns:
                if town['built']:
                    amount += approx_population_grow_per_week_in_town(
                        level, town['fort'], ext_dwellings, grail=False, legion_statue=False)

            # At least Citadel and dwelling is built
            towns[0]['fort'] = FortType.Citadel if towns[0]['fort'] == FortType.Fort else towns[0]['fort']
            towns[0]['built'] = True if level < 7 else towns[0]['built']

            if self.Trainer.Difficulty == Difficulty.Easy:
                ext_dwellings += self.Trainer.Random.int(0, 2)

            if self.Trainer.Difficulty == Difficulty.Medium:
                ext_dwellings += self.Trainer.Random.int(1, 2)

                if self.Trainer.Random.int(0, 1) == 0:
                    towns[0]['fort'] = FortType.Castle
                if self.Trainer.Random.int(0, 3) == 0:
                    towns[1]['fort'] = FortType.Citadel
                if self.Trainer.Random.int(0, 3) == 0:
                    towns[1]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Hard:
                ext_dwellings += self.Trainer.Random.int(2, 3)

                towns[0]['fort'] = FortType.Castle
                towns[1]['fort'] = FortType.Citadel
                towns[1]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Impossible:
                ext_dwellings += self.Trainer.Random.int(3, 5)

                towns[1]['fort'] = FortType.Castle
                towns[1]['built'] = True

            # Take into account extenral swellings
            amount += approx_external_dwelling_growth(level) * ext_dwellings

        week += 1

        if week == 3 and week <= weeks:

            # Compute on week growth
            for town in towns:
                if town['built']:
                    amount += approx_population_grow_per_week_in_town(
                        level, town['fort'], ext_dwellings, grail=False, legion_statue=False)

            # At least Castle and dwelling is built
            towns[0]['fort'] = FortType.Castle
            towns[0]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Easy:
                ext_dwellings += self.Trainer.Random.int(0, 2)

            if self.Trainer.Difficulty == Difficulty.Medium:
                ext_dwellings += self.Trainer.Random.int(0, 2)

                if self.Trainer.Random.int(0, 1) == 0:
                    towns[1]['fort'] = FortType.Citadel
                if self.Trainer.Random.int(0, 1) == 0:
                    towns[1]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Hard:
                ext_dwellings += self.Trainer.Random.int(0, 2)

                towns[1]['fort'] = FortType.Castle
                towns[1]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Impossible:
                ext_dwellings += self.Trainer.Random.int(1, 2)

            # Take into account extenral swellings
            amount += approx_external_dwelling_growth(level) * ext_dwellings

        week += 1

        if week == 4 and week <= weeks:

            # Compute on week growth
            for town in towns:
                if town['built']:
                    amount += approx_population_grow_per_week_in_town(
                        level, town['fort'], ext_dwellings, grail=False, legion_statue=False)

            if self.Trainer.Difficulty == Difficulty.Easy:
                ext_dwellings += self.Trainer.Random.int(0, 2)

            if self.Trainer.Difficulty == Difficulty.Medium:
                ext_dwellings += self.Trainer.Random.int(0, 2)

                towns[1]['fort'] = FortType.Castle
                towns[1]['built'] = True

            if self.Trainer.Difficulty == Difficulty.Hard:
                ext_dwellings += self.Trainer.Random.int(0, 1)

            if self.Trainer.Difficulty == Difficulty.Impossible:
                pass

            # Take into account extenral swellings
            amount += approx_external_dwelling_growth(level) * ext_dwellings

        week += 1

        while week <= weeks:
            for town in towns:
                if town['built']:
                    amount += approx_population_grow_per_week_in_town(
                        level, town['fort'], ext_dwellings, grail=False, legion_statue=False)
            amount += approx_external_dwelling_growth(level) * ext_dwellings
            week += 1

        if level <= 5:
            # Pandoras
            pand_count = self.Pandoras(weeks)
            if self.Trainer.verbose:
                print(f'Expecting pandoras of level {level}: {pand_count}')
            amount += approx_pandoras_army_by_level(level) * pand_count

        # Looses
        if self.Trainer.Difficulty == Difficulty.Easy:
            amount = math.ceil(amount * 0.75)
        if self.Trainer.Difficulty == Difficulty.Medium:
            amount = math.ceil(amount * 0.9)
        if self.Trainer.Difficulty == Difficulty.Hard:
            amount = amount
        if self.Trainer.Difficulty == Difficulty.Impossible:
            amount = math.ceil(amount * 1.25)

        amount = math.ceil(amount * coef)

        hero.AddCreature(slot, creature.name, amount)

        if self.Trainer.verbose:
            print(
                f'Hero {hero.Name} boosted with {creature.name} of amount {amount}')

    def Pandoras(self, week: int) -> int:
        # no more pandoras after 4 weeks
        if week >= 4:
            week = 4

        avg = math.ceil(min(week + self.Trainer.Difficulty.value,
                        self.Trainer.Random.int(5, 9)) / 2)

        return self.Trainer.Random.int(max(0, avg - self.Trainer.Random.int(1, 3)), avg + self.Trainer.Random.int(1, 3))


class JO_AIHeroBooster(HeroBooster):
    def setup_boosters(self):
        self.add_booster(JO_AIHeroArmyBooster)


# ----------------------------------------------------------- Actual trainer --

class JOMain(TheTemplateTrainer):

    # ------------------------------------------------------- Implementation --

    @property
    def id(self) -> str:
        return 'jo_main'

    @property
    def title(self) -> str:
        return 'Boost enemy army and hero on Jebus Outcast'

    def supported_templates(self) -> List[str]:
        return ['jebus_outcast_v2.81', 'jebus_outcast_v2.82', 'jebus_outcast_v2.83a', 'jebus_outcast_v2.96 test v1', 'jebus_outcast_v2.96a [1 Hero]', 'jebus_outcast_v2.96 test v2',]

    def check(self):
        # Somehow the generated map againts AIs still writes it has 4 humans!
        #if self.ScenarioInfo:
        #    if self.ScenarioInfo.HumanCount != 1:
        #        raise RuntimeError(
        #            'Current trainer supports only one human map')
        if self.Date is None:
            raise RuntimeError(
                    'Current trainer works only if Date is set')

    def run(self):
        self.player_color = player_color = self.get_player_hero()
        self.player_main = MostExperiencedHero(FilterByColor(
            self.Heroes, player_color))

        ais_colors = sorted([color for color in set(PlayersColors(self.Heroes)
                              ).difference({player_color}) if color is not None])
        self.ai_heroes = ai_heroes = [MostExperiencedHero(FilterByColor(
            self.Heroes, color)) for color in ais_colors]

        

        

        # VARIANT 1:
        ai_hero_booster = JO_AIHeroBooster(self)
        for ai_hero in ai_heroes:
            ai_hero_booster.boost(ai_hero)

        # ai_hero_booster.boost(self.player_main)

        # VARIANT 2:
        # ai_hero_booster = JO_AIHeroBooster
        # for ai_hero in ai_heroes:
        #    ai_hero_booster(self, ai_hero).boost()

    # ------------------------------------------------ Player identification --

    def guess_player_hero(self) -> Color:
        if days_passed(self.Date) < 3:
            raise RuntimeError(
                'Cannot identify player color from heroes as too small days passed')
        max_exp_hero = MostExperiencedHero(self.Heroes)
        return max_exp_hero.Color

    def get_player_hero(self) -> Color:
        player_color = None
        if self.ScenarioInfo:
            player_color = self.ScenarioInfo.MyselfColor

        if self.verbose:
            print('Cannot identify player from info, using heuristics')

        if not player_color:
            player_color = self.guess_player_hero()

        if not player_color:
            raise RuntimeError(
                'Missing infromation on scenario - cannot identify main hero')

        if self.verbose:
            print(f'Identified player color: {player_color}')

        return player_color

    def get_main_hero(self, color: Color) -> Optional[Hero]:
        return MostExperiencedHero(FilterByColor(self.Heroes, color))


class JOMainWithCenterTeleport(JOMain):
    @property
    def id(self) -> str:
        return 'jo_main_with_center_teleport'

    @property
    def title(self) -> str:
        return 'Boost enemy army and hero on Jebus Outcast plus teleport enemy to central town'

    def run(self):
        super().run()

        teleporter = TeleportCenter(self)
        # teleport_heroes = [MostExperiencedHero(self.ai_heroes)]
        teleport_heroes = self.ai_heroes
        teleporter.boost(teleport_heroes)


class JOMainWithTeleport(JOMain):
    @property
    def id(self) -> str:
        return 'jo_main_with_teleport'

    @property
    def title(self) -> str:
        return 'Boost enemy army and hero on Jebus Outcast plus teleport enemy near main hero'

    def run(self):
        super().run()

        teleporter = TeleportNearOther(self)
        # teleport_heroes = [MostExperiencedHero(self.ai_heroes)]
        teleport_heroes = self.ai_heroes
        teleporter.boost(teleport_heroes, self.player_main)


class JOMainWithSmartTeleoprt(JOMain):
    pass


if False:
    class JebusOutcastTrainer(TheTrainer):

        @property
        def name(self):
            return 'jebus_outcast'

        def for_template(self, template: str):
            if template == 'jebus_outcast':
                return True
            return False

        def BoostSuppoorted(self) -> List[str]:
            return ['boost_ai']

        def BoostAllAIHeroes(self):
            raise NotImplementedError()

        def BoostAIHero(self, ):
            raise NotImplementedError()

        def BoostYourself(self):
            raise NotImplementedError()

        def SkillizeHero(self, hero: Hero):
            raise NotImplementedError()

        def ArmyizeHero(self, hero: Hero):
            hero.CleanCreatures()
            creatures = hero.Town().AllCreatures()

            days = days_passed(self.Date)

            for level, creature_variants in creatures.items():
                upg = creature_variants.keys()
                key = random.choice(upg)
                creature = creature_variants[key]

                amount = (7-level + 1) * days

                hero.SetCreature(slot=level, creature=creature, amount=amount)

        def ArtifactizeHero(self, hero: Hero):
            raise NotImplementedError()

        def TeleportAIHero(self, hero: Hero):
            raise NotImplementedError()

        def SkillizeAIHero(self):
            raise NotImplementedError()

        def SkillizeYourself(self):
            raise NotImplementedError()

    def SkillizeJebusOutcast(date: Date, hero: Hero):

        pass
