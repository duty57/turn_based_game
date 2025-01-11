import logging
import os
import sys

import pygame

from turn_based_game.Camera import Camera
from turn_based_game.Game import Game
from turn_based_game.LoadCharacters import character_init_warrior, character_init_healer, character_init_archer, character_init_enemy
from turn_based_game.LoadCharacters import character_init_wizard
from turn_based_game.Renderer import Renderer


pygame.init()
game = Game()
camera = Camera(1280, 1000, 1280, 720)


Warrior = character_init_warrior(200, 300)
Wizard = character_init_wizard()
Healer = character_init_healer()
Archer = character_init_archer()


Skeleton = character_init_enemy('Skeleton', 0, 0, Warrior)
Goblin = character_init_enemy('Goblin', 500, 360, Warrior)

game.add_main_character(Warrior)
game.add_characters([Warrior, Healer])
enemy_objects = [Goblin]

game.add_enemies(enemy_objects)
game.add_camera(camera)

game.run(1280, 720, False)

pygame.quit()
