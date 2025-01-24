class Item:
    def __init__(self, name, quantity):

        self.quantity = quantity

        self.item_type = None
        self.name = name
        self.description = None
        self.image = None

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description)

    def set_image(self, image):
        self.image = image
