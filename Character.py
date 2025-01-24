import pygame
from Enums import CharacterBattleState, CharacterState
from turn_based_game.Actor import Actor
from turn_based_game.CharacterController import CharacterController


class Character(Actor):

    def __init__(self, config_file: str, character_name: str, x: int = 200, y: int = 100):
        # Character States
        super().__init__(config_file, character_name, x, y)
        self.controller = CharacterController(self, x, y)

    def level_up(self):
        self.level += 1

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.nextLevel:
            self.level_up()
            self.experience = 0
            self.nextLevel += 100 * self.level

    def play(self, window, keys, adjusted_rect=None, collisions=None):
        self.controller.controller(window, keys, self.rect, adjusted_rect, collisions)
