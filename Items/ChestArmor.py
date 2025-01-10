import json

from turn_based_game.Items.Item import Item


class ChestArmor(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.protection = data[name]['protection']
            self.defenseBonus = data[name]['defenseBonus']
            self.HPBonus = data[name]['HPBonus']
            self.speedBonus = data[name]['speedBonus']
            self.agilityBonus = data[name]['agilityBonus']
            self.actionPointsBonus = data[name]['actionPointsBonus']
            self.immunity = data[name]['immunity']