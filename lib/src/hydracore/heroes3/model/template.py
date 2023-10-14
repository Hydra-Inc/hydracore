from abc import ABC, abstractmethod
from typing import Optional, List

from .map import MapBannedInfo, NolimitsMap


class Template(ABC):

    def template(self):
        pass

    @abstractmethod
    def id(self) -> str:
        """
        Returns short name of the template without version
        """
        raise NotImplementedError()

    @abstractmethod
    def name(self) -> str:
        """
        Returns name of the template as a string without version
        """
        raise NotImplementedError()

    @abstractmethod
    def version(self) -> str:
        """
        Returns version of the template
        """
        raise NotImplementedError()

    def fullname(self) -> str:
        return self.name() + ' v' + self.version()

    def fullid(self) -> str:
        return self.id() + '_v' + self.version()

    def identify_template(self,
                          title: Optional[str] = None,
                          description: Optional[str] = None,
                          map_file: Optional[str] = None) -> bool:
        ver = ' '+self.version() + ','
        return self.name() in description and ver in description

    def banned_info(self) -> MapBannedInfo:
        """
        Get information on Banned speels and artifacts on this template
        """
        return NolimitsMap()


class TemplateList:

    def __init__(self):
        self.build_list()

    def build_list(self):
        from ..templates import list_templates
        self._all = list_templates()
        self._extended = {}
        for t in self._all:
            tpl = t()
            self._extended[tpl.fullid()] = {
                'class': t,
                'object': tpl,
                'name': tpl.fullname()
            }

    def get_ids(self) -> List[str]:
        return [x for x in self._extended.keys()]

    def identify_template(self,
                          title: Optional[str] = None,
                          description: Optional[str] = None,
                          map_file: Optional[str] = None) -> Optional[Template]:
        """
        Identifies template from title, description, map file name.
        """
        for k, tpl in self._extended.items():
            if tpl['object'].identify_template(title, description, map_file):
                return tpl['object']
        return None
