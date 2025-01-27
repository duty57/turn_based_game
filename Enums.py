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


class CharacterState(Enum):
    idle = 1
    moving = 2
    attacking = 3
    hit = 4
    healing = 5
    dead = 6
    inactive = 7


class CharacterBattleState(Enum):
    init = 0
    idle = 1
    attacking = 2
    back_in_position = 3


class SelectionMode(Enum):
    enemy = 1
    character = 2
    items = 3
    skills = 4
