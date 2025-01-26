import random

import pygame
import pygame.mixer
from turn_based_game.LoadCharacters import character_init_enemy
from turn_based_game.World_Renderer import WorldRenderer
from turn_based_game.Battle import Battle
from turn_based_game.Level import enemy_list
from Enums import Initiative

pygame.mixer.init()

ambient_music = pygame.mixer.Sound('turn_based_game/audio/ambient_world.mp3')

class Game:

    def __init__(self):
        self.characters = None
        self.window = None
        self.renderer = WorldRenderer()
        self.clock = pygame.time.Clock()
        self.objects = pygame.sprite.Group()
        self.main_character = None
        self.enemies = []
        self.is_in_battle = False
        self.battle = None

        self.camera = None
        self.level = None

        self.inventory = None
        self.opponent = None

    def add_objects(self, objects):
        self.objects.add(objects)

    def add_enemies(self, enemies):#add enemies to the game(level)
        for enemy in enemies:
            enemy.controller.set_main_character(self.main_character)
        self.objects.add(enemies)

    def add_characters(self, characters):
        self.characters = characters
        self.main_character = characters[0]
        self.objects.add(self.main_character)
        self.renderer.characters = characters

    def add_camera(self, camera):
        self.camera = camera
        self.renderer.set_camera(camera)

    def add_level(self, level):#add level to the game
        self.level = level
        self.renderer.set_level(level)
        self.add_enemies(level.get_enemies())

    def create_window(self, width, height, fullscreen=False):
        self.window = pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else 0, pygame.DOUBLEBUF)
        self.renderer.create_window(self.window)
        # ambient_music.play(10)
        # ambient_music.set_volume(0.1)

    def get_collision_rect(self):
        collision_rect = []
        for row_index, row in enumerate(self.level.tile_map_world):
            for col_index, tile in enumerate(row):
                if 20 < tile < 40:
                    collision_rect.append(
                        pygame.Rect(col_index * self.level.tile_width, row_index * self.level.tile_height,
                                    self.level.tile_width, self.level.tile_height))
        return collision_rect

    def detect_collision(self, character):
        collided_objects = pygame.sprite.spritecollide(character, self.objects, False)
        for obj in collided_objects:
            if obj != character and character.controller.finished_attack:
                self.enemies.append(obj)
                obj.controller.collide()
                self.start_battle(Initiative.player_initiative)
                character.controller.is_hit = False
                self.opponent = obj
            elif obj != character and obj.is_enemy() and obj.controller.finished_attack:
                self.enemies.append(obj)
                self.start_battle(Initiative.enemy_initiative)
                character.controller.is_hit = False
                self.opponent = obj

    def generate_enemy_team(self):
        self.enemies.append(character_init_enemy(random.choice(enemy_list), 0, 0, self.main_character))
        self.enemies.append(character_init_enemy(random.choice(enemy_list), 0, 0, self.main_character))

    def start_battle(self, initiative=Initiative.player_initiative):
        turn_order = []
        self.is_in_battle = True
        self.generate_enemy_team()

        # calculate turn order
        if initiative == Initiative.player_initiative:
            for character in self.characters:
                turn_order.append(character)
            for enemy in self.enemies:
                turn_order.append(enemy)
        else:
            for enemy in self.enemies:
                turn_order.append(enemy)
            for character in self.characters:
                turn_order.append(character)

        self.battle = Battle(self.window, self.characters, self.enemies, initiative, turn_order)
        self.battle.start()

    def run(self, width, height, fullscreen=False):
        self.create_window(width, height, fullscreen)
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.main_character.controller.in_battle:
                # character_rect = pygame.Rect(self.main_character.controller.x - 15, self.main_character.controller.y - 20, 30, 40)
                if self.opponent: #clear defeated enemies
                    for enemy in self.enemies:
                        self.objects.remove(enemy)
                    self.enemies.clear()

                self.main_character.play(window=self.window, collisions=self.get_collision_rect())  # Character controller
                self.renderer.camera.update(self.main_character)  # Update camera position
                self.detect_collision(self.main_character)  # Detect collision
                for obj in self.objects:
                    if obj.is_enemy():
                        obj.play(window=self.window, adjusted_rect=pygame.Rect(0, 0, 1280, 720))
                self.renderer.draw(objects=self.objects)  # Draw objects

            else:
                ambient_music.stop()
                self.battle.draw()
        pygame.quit()
