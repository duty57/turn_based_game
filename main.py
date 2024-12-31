import pygame

from turn_based_game.Camera import Camera
from turn_based_game.Game import Game
from turn_based_game.LoadCharacters import character_init_warrior, character_init_healer, character_init_archer, character_init_enemy
from turn_based_game.LoadCharacters import character_init_wizard
from turn_based_game.Renderer import Renderer

game = Game()
camera = Camera(1280, 1000, 1280, 720)


Warrior = character_init_warrior(200, 300)
Skeleton = character_init_enemy('Skeleton', 0, 0, Warrior)
Goblin = character_init_enemy('Goblin', 500, 360, Warrior)
# Wizard = character_init_wizard()
# Healer = character_init_healer()
# Archer = character_init_archer()

game.add_main_character(Warrior)
game_objects = [ Goblin]

game.add_objects(game_objects)
game.add_camera(camera)

game.run(1280, 720, True)


pygame.quit()
