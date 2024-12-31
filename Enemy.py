from math import sqrt
from time import sleep

import pygame

from turn_based_game.Character import Character


class Enemy(Character):
    def __init__(self, config, characterName, x, y, main_character=None):
        super().__init__(config, characterName, x, y)
        self.enemy = True

        self.patrol_points = [(x+100, y), (x-100, y), (x, y)]
        self.current_patrol_point = 0

        self.is_triggered = False
        self.main_character = main_character

        self.trigger_time = None

    def moveRight(self):
        self.x += 1
        self.moving_right_direction = True
        self.moving_left_Direction = False
        self.idling = False


    def moveLeft(self):
        self.x -= 1
        self.moving_right_direction = False
        self.moving_left_Direction = True
        self.idling = False

    def moveUp(self):
        self.y -= 1
        self.idling = False

    def moveDown(self):
        self.y += 1
        self.idling = False

    def set_main_character(self, main_character):
        self.main_character = main_character

    def trigger(self):
        if abs(self.x - self.main_character.x)**2 + abs(self.y - self.main_character.y)**2 < 25**2:
            if self.trigger_time is None:
                self.trigger_time = pygame.time.get_ticks()  # Record the time when the enemy is triggered
            elif pygame.time.get_ticks() - self.trigger_time > 500:  # If 1 second has passed since the enemy was triggered
                self.attacking = True
                self.main_character.collide()
                self.trigger_time = None
        elif abs(self.x - self.main_character.x)**2 + abs(self.y - self.main_character.y)**2 < 100**2:
            self.is_triggered = True
            self.patrol_points[-1] = (self.main_character.x, self.main_character.y)
            self.current_patrol_point = 2
        elif self.is_triggered:
            self.is_triggered = False
            self.current_patrol_point = 0

    def controller(self):
        #patrol the area

        if not self.attacking:
            if self.x < self.patrol_points[self.current_patrol_point][0]:
                self.moveRight()
                if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
                    self.moveDown()
                elif self.y - 10 > self.patrol_points[self.current_patrol_point][1]:
                    self.moveUp()

            elif self.x > self.patrol_points[self.current_patrol_point][0]:
                self.moveLeft()
                if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
                    self.moveDown()
                elif self.y - 10 > self.patrol_points[self.current_patrol_point][1]:
                    self.moveUp()
            else:
                self.current_patrol_point = (self.current_patrol_point + 1) % (len(self.patrol_points) - 1)
        self.rect.topleft = (self.x, self.y)
        self.trigger()

#TODO: Attack animation when is closer than 25 pixels
#TODO: Register collision with main character