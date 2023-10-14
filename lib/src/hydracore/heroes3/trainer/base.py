from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from typing import List, Optional, Union


from .random import RandomTech

from ..model.hero import Hero
from ..model.time import Date
from ..model.map import MapBannedInfo as _MapBannedInfo, MapTerrainInfo as _MapTerrainInfo
from ..model.scenario import ScenarioInfo as _ScenarioInfo


class Difficulty(Enum):
    Easy = 1
    Medium = 2
    Hard = 3
    Impossible = 4

    


class Trainer(ABC):

    def trainer(self):
        """ marker for the list engine to work """

    # ---------------------------------------------------- Overwrite methods --

    @property
    @abstractproperty
    def id(self) -> str:
        """
        Returns trainer full id
        """
        raise NotImplementedError()

    @property
    @abstractproperty
    def title(self) -> str:
        """
        Returns trainer title
        """
        raise NotImplementedError()

    @abstractmethod
    def run(self):
        """
        Main method to apply the trainer to provided setup
        """
        raise NotImplementedError()
    
    @abstractmethod
    def check(self):
        """
        Returns True is the trainer could be used on this data, otherwise raises
        error
        """
        raise NotImplementedError()
    
    # -------------------------------------------------------------- Getters --

    @property
    def MapBannedInfo(self) -> Optional[_MapBannedInfo]:
        raise NotImplementedError()

    @property
    def MapTerrainInfo(self) -> Optional[_MapTerrainInfo]:
        raise NotImplementedError()

    @property
    def ScenarioInfo(self) -> Optional[_ScenarioInfo]:
        raise NotImplementedError()

    @property
    def Date(self) -> Date:
        raise NotImplementedError()

    @property
    def Heroes(self) -> List[Hero]:
        raise NotImplementedError()

    @property
    def Difficulty(self) -> Difficulty:
        raise NotImplementedError()

    # -------------------------------------------------------------- Setters --

    def SetMapBannedInfo(self, v: Optional[_MapBannedInfo]):
        raise NotImplementedError()

    def SetMapTerrainInfo(self, v: Optional[_MapTerrainInfo]):
        raise NotImplementedError()

    def SetScenarioInfo(self, v: Optional[_ScenarioInfo]):
        raise NotImplementedError()

    def SetDate(self, v: Date):
        raise NotImplementedError()

    def SetHeroes(self, v: List[Hero]):
        raise NotImplementedError()

    def SetDifficulty(self, v: Difficulty):
        raise NotImplementedError()
    
    def SetVerbose(self):
        raise NotImplementedError()
    
    # ----------------------------------------------------------- Interfaces --

    @property
    def Random(self) -> RandomTech:
        raise NotImplementedError()

    def SetRandomTech(self, randtech: RandomTech):
        raise NotImplementedError()


class TemplateTrainer(ABC):

    @abstractmethod
    def supported_templates(self) -> List[str]:
        """
        List of templates that this trainer supports.

        We return the list of template fullids, explicitly so we may be sure, that
        everything is working for this template.

        TODO: if needed we may later process this list not by full list and etc.
              but for now lets work each version of template directly.
        """
        raise NotImplementedError()


# ----------------------------------------------------------- Implementation --


class TheTrainer(Trainer):

    def __init__(self):
        self._map_banned_info = None
        self._map_terrain_info = None
        self._scenario_info = None
        self._date = None
        self._heroes = None
        self._difficulty = None
        self._verbose = None

        self._random = RandomTech()

    @property
    def MapBannedInfo(self) -> Optional[_MapBannedInfo]:
        return self._map_banned_info

    @property
    def MapTerrainInfo(self) -> Optional[_MapTerrainInfo]:
        return self._map_terrain_info

    @property
    def ScenarioInfo(self) -> Optional[_ScenarioInfo]:
        return self._scenario_info

    @property
    def Date(self) -> Date:
        return self._date

    @property
    def Heroes(self) -> List[Hero]:
        return self._heroes

    @property
    def Difficulty(self) -> Difficulty:
        return self._difficulty
    
    @property
    def verbose(self) -> bool:
        return self._verbose

    # -------------------------------------------------------------- Setters --

    def SetMapBannedInfo(self, v: Optional[_MapBannedInfo]):
        self._map_banned_info = v

    def SetMapTerrainInfo(self, v: Optional[_MapTerrainInfo]):
        self._map_terrain_info = v

    def SetScenarioInfo(self, v: Optional[_ScenarioInfo]):
        self._scenario_info = v

    def SetDate(self, v: Date):
        self._date = v

    def SetHeroes(self, v: List[Hero]):
        self._heroes = v

    def SetDifficulty(self, v: Difficulty):
        self._difficulty = v

    def SetVerbose(self):
        self._verbose = True

    @property
    def Random(self) -> RandomTech:
        return self._random

    def SetRandomTech(self, randtech: RandomTech):
        self._random = randtech


class TheTemplateTrainer(TheTrainer, TemplateTrainer):
    pass


if False:

    class Trainer1:

        def setup(self,
                  map_info: Optional[MapInfo],
                  scenario_info: Optional[ScenarioInfo],
                  date: Date,
                  heroes: List[Hero],
                  difficulty: Difficulty):
            raise NotImplementedError()

        @property
        def name(self):
            raise NotImplementedError()

        @property
        def MapInfo(self) -> MapInfo:
            raise NotImplementedError()

        @property
        def ScenarioInfo(self) -> ScenarioInfo:
            raise NotImplementedError()

        @property
        def Date(self) -> Date:
            raise NotImplementedError()

        @property
        def Heroes(self) -> List[Hero]:
            raise NotImplementedError()

        def for_template(self, template: str):
            raise NotImplementedError()

        def BoostSuppoorted(self) -> List[str]:
            """
            Returns list of what is possible to boost for this Trainer:
            """
            raise NotImplementedError()

        def BoostAllAIHeroes(self):
            raise NotImplementedError()

        def BoostAIHero(self, ):
            raise NotImplementedError()

        def BoostYourself(self):
            raise NotImplementedError()

        def SkillizeHero(self, hero: Hero):
            raise NotImplementedError()

        def ArmyizeHero(self, hero: Hero):
            raise NotImplementedError()

        def ArtifactizeHero(self, hero: Hero):
            raise NotImplementedError()

        def TeleportAIHero(self, hero: Hero):
            raise NotImplementedError()

    def get_trainer(name: str,
                    map_info: MapInfo,
                    scenario_info: ScenarioInfo,
                    date: Date,
                    heroes: List[Hero],
                    difficulty: Difficulty) -> Trainer:

        trainers = list_trainers()
        if not name in trainers:
            raise RuntimeError(f'Trainer {name} not found')

        trainer = trainers[name]()
        trainer.setup(map_info=map_info,
                      scenario_info=scenario_info,
                      date=date,
                      heroes=heroes,
                      difficulty=difficulty)

        return trainer

    # ----------------------------------------------------------- Implementation --

    class TheTrainer:

        def setup(self,
                  map_info: MapInfo,
                  scenario_info: ScenarioInfo,
                  date: Date,
                  heroes: List[Hero],
                  difficulty: Difficulty):
            """
            Later to add towns and etc...S        
            """
            self._map_info = map_info
            self._scenario_info = scenario_info
            self._date = date
            self._heroes = heroes
            self._difficulty = difficulty

        @property
        def MapInfo(self) -> MapInfo:
            return self._map_info

        @property
        def ScenarioInfo(self) -> ScenarioInfo:
            return self._scenario_info

        @property
        def Date(self) -> Date:
            return self._date

        @property
        def Heroes(self) -> List[Hero]:
            return self._heroes

        def BoostSuppoorted(self) -> List[str]:
            """
            Returns list of what is possible to boost for this Trainer:
            """
            raise NotImplementedError()

        def BoostAllAIHeroes(self):
            raise NotImplementedError()

        def BoostAIHero(self, ):
            raise NotImplementedError()

        def BoostYourself(self):
            raise NotImplementedError()

        def SkillizeHero(self, hero: Hero):
            raise NotImplementedError()

        def ArmyizeHero(self, hero: Hero):
            raise NotImplementedError()

        def ArtifactizeHero(self, hero: Hero):
            raise NotImplementedError()

        def TeleportAIHero(self, hero: Hero):
            raise NotImplementedError()
