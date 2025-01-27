import json

from turn_based_game.Items.Item import Item


class Weapon(Item):
    def __init__(self, name, rarity, quantity):
        super().__init__(name, quantity)
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.damage = data['weapon'][rarity][name]['damage']
            self.rarity = rarity
            self.HPBonus = data['weapon'][rarity][name]['HPBonus']
            self.actionPointsBonus = data['weapon'][rarity][name]['actionPointsBonus']
            self.set_image(f'turn_based_game/assets/Items/Weapons/{name}.png')
