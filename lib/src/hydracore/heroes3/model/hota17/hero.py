from ..hota.hero import HOTAHero


class HOTA17Hero(HOTAHero):

    def __init__(self):
        super().__init__('hota17')
        self._cannon = False

    def hero_attrs(self):
        return HOTA17Hero().__dict__.keys()

TheHero=HOTA17Hero
