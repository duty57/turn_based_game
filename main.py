import pygame

from turn_based_game.Camera import Camera
from turn_based_game.Game import Game
from turn_based_game.Level import Level
from turn_based_game.LoadCharacters import init_character, character_init_enemy
from turn_based_game.World_Renderer import WorldRenderer


pygame.init()
pygame.mixer.init()
game = Game()
level = Level()
camera = Camera(1280, 1000, 1280, 720)

Warrior = init_character('Warrior', 200, 300, True, (64, 48))
Healer = init_character('Witch', 200, 300)
Wizard = init_character('Wizard', 200, 300, True, (40, 40))
Archer = init_character('Archer', 200, 300)



game.add_characters([Warrior, Healer, Wizard, Archer])

game.add_camera(camera)
game.add_level(level)

game.run(1280, 720, False)

pygame.quit()
