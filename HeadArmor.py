import json
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
class HeadArmor:
    def __init__(self, name):
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.name = name
            self.protection = data[name]['protection']
            self.image = data[name]['image']
            self.defenseBonus = data[name]['defenseBonus']
            self.HPBonus = data[name]['HPBonus']
            self.speedBonus = data[name]['speedBonus']
            self.agilityBonus = data[name]['agilityBonus']
            self.actionPointsBonus = data[name]['actionPointsBonus']
            self.immunity = data[name]['immunity']
