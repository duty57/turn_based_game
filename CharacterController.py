import pygame
from turn_based_game.Controller import Controller

class CharacterController(Controller):

        def __init__(self, actor):
            super().__init__(actor)

            self.walkRight = self.actor.animations['move_right']
            self.idle = self.actor.animations['idle']
            self.attack = self.actor.animations['attack']
            self.damageTaken = self.actor.animations['hit']
