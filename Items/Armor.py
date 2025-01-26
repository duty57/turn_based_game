import json

from turn_based_game.Items.Item import Item

#chest armor, helmet, boots
class Armor(Item):

    def __init__(self, name, quantity):
        super().__init__(name, quantity)
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.item_type = data[name]['item_type']
            self.description = data[name]['description']
            self.protection = data[name]['protection']
            self.defenseBonus = data[name]['defenseBonus']
            self.HPBonus = data[name]['HPBonus']
            self.speedBonus = data[name]['speedBonus']
            self.agilityBonus = data[name]['agilityBonus']
            self.actionPointsBonus = data[name]['actionPointsBonus']
            self.immunity = data[name]['immunity']