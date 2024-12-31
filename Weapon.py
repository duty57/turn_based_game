import json
class Weapon:
    def __init__(self, name):
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.name = name
            self.damage = data[name]['damage']
            self.image = data[name]['image']
            self.category = data[name]['category']