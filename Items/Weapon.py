import json

from turn_based_game.Items.Item import Item


class Weapon(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.damage = data[name]['damage']
            self.category = data[name]['category']