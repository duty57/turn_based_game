import pygame

from turn_based_game.Actors.Actor import Actor
from turn_based_game.Controllers.EnemyController import EnemyController
from turn_based_game.Actors.Character import Character


class Enemy(Actor):
    def __init__(self, config: str, character_name: str, x: int, y: int, main_character: Character = None):
        super().__init__(config, character_name, x, y)
        self.controller = EnemyController(self, x, y, main_character)

    def play(self, window: pygame.Surface, adjusted_rect: pygame.Rect = None):
        self.controller.controller(window, adjusted_rect)