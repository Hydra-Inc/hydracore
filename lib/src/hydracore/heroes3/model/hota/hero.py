from ..hero import Hero


class HOTAHero(Hero):

    def __init__(self):
        super().__init__('hota')
        self._cannon = False

    @property
    def Cannon(self) -> bool:
        return self._cannon
    
    @Cannon.setter
    def Cannon(self, x):
        self._cannon = x
    
    def dump_items(self):
        it = []
        if self._ammocart:
            it.append('Ammo Cart')
        if self._ballista:
            it.append('Ballista')
        if self._first_aid_tent:
            it.append('First Aid Tent')
        if self._cannon:
            it.append('Cannon')
        if not it:
            it.append('-none-')
        print(f'  Items: '+','.join(it))

    
    def _init_state(self):
        super()._init_state()
        self._stored_states['items']['fields'].append('_cannon')

    def hero_attrs(self):
        return HOTAHero().__dict__.keys()

TheHero=HOTAHero
