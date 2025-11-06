import json

from Items.Item import Item


class Weapon(Item):
    def __init__(self, name: str, rarity: str):
        super().__init__(name)
        with open('config/itemStats.json') as file:
            data = json.load(file)
            self.damage = data['weapon'][rarity][name]['damage']
            self.item_type = data['weapon'][rarity][name]['item_type']
            self.rarity = rarity
            self.HPBonus = data['weapon'][rarity][name]['HPBonus']
            self.actionPointsBonus = data['weapon'][rarity][name]['actionPointsBonus']
            self.set_image(f'assets/Items/Weapons/{name}.png')

    def get_stats(self):
        return f"DMG: {self.damage} HP: {self.HPBonus}  AP: {self.actionPointsBonus}"
