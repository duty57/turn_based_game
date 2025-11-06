import json
import random

import pygame

from Dataclasses.GameUI import GameUI as UI
from Items.Armor import Armor
from Items.Weapon import Weapon

chest_types = ["common", "equipment", "legendary"]

probabilities = {
    "common": [75, 20, 5],
    "equipment": [25, 65, 10],
    "legendary": [15, 55, 40]
}


class Chest(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.name = "Chest"
        self.x = x
        self.y = y
        self.chest_type = random.choice(chest_types)
        self.image = UI.chests[self.chest_type]
        self.opening_animation = UI.chest_animation[self.chest_type]
        self.probabilities = probabilities[self.chest_type]
        self.frame = 0
        self.item = None
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __del__(self):
        print("Chest deleted")

    def is_enemy(self):
        return False

    def get_item(self):
        return self.item
    def open(self):
        self.generate_item()

    def generate_item(self):# Generate item based on probabilities
        rarity_chance = random.randint(1, 100)
        category_chance = random.randint(1, 100)
        if rarity_chance <= self.probabilities[0]:
            rarity = "common"
        elif rarity_chance <= self.probabilities[0] + self.probabilities[1]:
            rarity = "rare"
        else:
            rarity = "legendary"

        if category_chance <= 70:
            category = "armor"
        else:
            category = "weapon"

        with open('config/itemStats.json') as file:
            data = json.load(file)
            item_name = data[category][rarity]
            random_item = random.choice(list(item_name))
            if category == "armor":
                self.item = Armor(random_item, rarity)
            else:
                self.item = Weapon(random_item, rarity)
