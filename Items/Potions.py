from turn_based_game.Items.Item import Item


class Potion(Item):
    def __init__(self, name, description):
        super().__init__(name, description)
        self.healing = 0
        self.actionPointsBonus = 0
        self.immunity = None