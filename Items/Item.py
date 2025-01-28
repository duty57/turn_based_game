import pygame


class Item:
    def __init__(self, name: str):
        self.item_type = None
        self.rarity = None
        self.name = name
        self.description = None
        self.image = None
        self.rect = None
        self.owner = None
        self.is_equipped = False

    def set_image(self, path: str):
        self.image = pygame.image.load(path)
