from enum import Enum

class elements(Enum):
    SLASH = 1
    PIERCE = 2
    MAGIC = 3
    FIRE = 4
    ICE = 5
    WIND = 6
    LIGHT = 7
    DARK = 8
class Initiative(Enum):
    player_initiative = 1
    enemy_initiative = 2