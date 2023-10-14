import re

from typing import List, Optional

from .arch import Color


class ScenarioInfo:

    @property
    def HumanCount(self) -> Optional[int]:
        """
        How much humans
        """
        raise NotImplementedError()

    @property
    def MyselfColor(self) -> Optional[Color]:
        """
        Color of yourself
        """
        raise NotImplementedError()

    @property
    def HumanColors(self) -> Optional[List[Color]]:
        """
        All available player colors
        """
        raise NotImplementedError()

    @property
    def AIColors(self) -> Optional[List[Color]]:
        """
        Color of AI players
        """
        raise NotImplementedError()


def maybe_scenario_info(title: Optional[str] = None,
                        description: Optional[str] = None) -> Optional[ScenarioInfo]:
    """
    Get some information from scenraio title and description.
    This is possible only if the map was generated from template
    """
    return _maybe_scenario_info(title, description)


# ----------------------------------------------------------- Implementation --

def _maybe_scenario_info(title: Optional[str] = None,
                         description: Optional[str] = None) -> Optional[ScenarioInfo]:
    """
    Example:
    Map created by the Random Map Generator.
    Template was Jebus Outcast from pack Jebus Outcast 2.83a, Random seed was 1682989697, size 144, levels 1, humans 1, computers 3, water None, monsters 3, HotA 1.6.1 expansion map, red is human, red town choice is inferno
    """
    scenario = TheScenarioInfo()

    m = re.search(r'humans ([\d]+),', description)
    if not m:
        return None

    scenario.SetHumanCount(int(m.group(1)))

    m = re.search(r'([a-zA-Z]+) is human,', description)
    if m:
        scenario.SetMyselfColor(Color.from_str(str(m.group(1))))

    return scenario


class TheScenarioInfo(ScenarioInfo):

    def __init__(self):
        self._human_count = None
        self._myself_color = None
        self._human_colors = None
        self._ai_colors = None

    @property
    def HumanCount(self) -> Optional[int]:
        return self._human_count

    @property
    def MyselfColor(self) -> Optional[Color]:
        return self._myself_color

    @property
    def HumanColors(self) -> Optional[List[Color]]:
        return self._human_colors

    @property
    def AIColors(self) -> Optional[List[Color]]:
        return self._ai_colors

    def SetHumanCount(self, v: int):
        self._human_count = v

    def SetMyselfColor(self, v: Color):
        self._myself_color = v

    def SetHumanColors(self, v: List[Color]):
        self._human_colors = v

    def SetAIColors(self, v: List[Color]):
        self._ai_colors = v
