from Items.Item import Item


class Potion(Item):
    def __init__(self, name, quantity):
        super().__init__(name, quantity)
        self.item_type = 'Potion'