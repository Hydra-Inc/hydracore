from enum import Enum


class Slot(str, Enum):
    helm = 'helm'
    neck = 'neck'
    armor = 'armor'
    weapon = 'weapon'
    shield = 'shield'
    hand = 'hand'
    cloak = 'cloak'
    feet = 'feet'
    side = 'side'
    inventory = 'inventory'

    def to_str(slot: 'Slot'):
        return str(slot).replace('Slot.','')


class Color(Enum):
    Red = 1
    Blue = 2
    Tan = 3
    Green = 4
    Orange = 5
    Purple = 6
    Teal = 7
    Pink = 8
    
    def to_str(color: 'Color'):
        return str(color).replace('Color.','')

    def from_str(color: str) -> 'Color':
        if color == 'red': return Color.Red
        if color == 'blue': return Color.Blue
        if color == 'tan': return Color.Tan
        if color == 'green': return Color.Green
        if color == 'orange': return Color.Orange
        if color == 'purple': return Color.Purple
        if color == 'teal': return Color.Real
        if color == 'pink': return Color.Pink
        return None

    
class Player(Enum):
    Human = 'Human'
    Computer = 'Computer'

    def to_str(player: 'Player'):
        return str(player).replace('Player.','')
