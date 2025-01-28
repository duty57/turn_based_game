import json

from turn_based_game.Items.Item import Item

#chest armor, helmet, boots
class Armor(Item):

    def __init__(self, name: str, rarity: str):
        super().__init__(name)
        with open('turn_based_game/config/itemStats.json') as file:
            data = json.load(file)
            self.item_type = data['armor'][rarity][name]['item_type']
            self.description = data['armor'][rarity][name]['description']
            self.rarity = rarity
            self.defenseBonus = data['armor'][rarity][name]['defenseBonus']
            self.HPBonus = data['armor'][rarity][name]['HPBonus']
            self.agilityBonus = data['armor'][rarity][name]['agilityBonus']
            self.actionPointsBonus = data['armor'][rarity][name]['actionPointsBonus']
            self.set_image(f'turn_based_game/assets/Items/Armor/{name}.png')

    def get_stats(self):
        return f"DEF: {self.defenseBonus} HP: {self.HPBonus}  AP: {self.actionPointsBonus}  AGI: {self.agilityBonus}"
