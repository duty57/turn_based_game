from turn_based_game.Actors.Actor import Actor
from turn_based_game.Controllers.EnemyController import EnemyController


class Enemy(Actor):
    def __init__(self, config, character_name, x, y, main_character=None):
        super().__init__(config, character_name, x, y)
        self.controller = EnemyController(self, x, y, main_character)

    def play(self, window, adjusted_rect=None):
        self.controller.controller(window, adjusted_rect)
