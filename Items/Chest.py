import random
from turn_based_game.GameUI import GameUI as UI

chest_types = ["common", "equipment", "legendary"]

class Chest:
    def __init__(self):

        self.chest_type = random.choice(chest_types)
        self.image = UI.chests[self.chest_type]
        self.opening_animation = UI.chest_animation[self.chest_type]
        self.frame = 0
        self.item = None
    def play_opening_animation(self, window, x, y):
        window.blit(self.opening_animation[self.frame], (x, y))
        self.frame += 1
        if self.frame >= len(self.opening_animation):
            self.frame = 0
            return True
        return False

    def generate_item(self):
        pass