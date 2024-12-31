import json

class Shoes:
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
            self.element = data[name]['element']
