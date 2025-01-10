class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.image = None

    def __str__(self):
        return "{}\n=====\n{}\nValue: {}\n".format(self.name, self.description)

    def set_image(self, image):
        self.image = image
