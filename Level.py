import random

import pygame
from turn_based_game.LoadCharacters import character_init_enemy
from turn_based_game.Items.Chest import Chest

enemy_list = ['Skeleton', 'Goblin', 'Flying_demon']


class Level:

    def __init__(self):
        self.tile_map_world = []
        self.tile_map_battle = []
        self.tile_width = 64
        self.tile_height = 64

        # 0-10 common tiles
        # 11-20 tiles with flowers
        # 21-30 horizontal walls
        # 31-40 vertical walls
        # 41-50 background tiles
        # 69 - enemy spawn point
        self.tiles = {
            10: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_1.png'),
            21: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Horizontal_1.png'),
            22: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Horizontal_2.png'),
            31: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Vertical_1.png'),
            32: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Vertical_2.png'),
            33: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Corner_Outside_1.png'),
            34: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Corner_Outside_2.png'),
            35: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Corner_Outside_3.png'),
            36: pygame.image.load('turn_based_game/assets/Map/Walls/Wall_Corner_Outside_4.png'),
            11: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_2.png'),
            12: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_3.png'),
            13: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_7.png'),
            14: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_8.png'),
            40: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_6.png'),
            57: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_4.png'),
            69: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_5.png')
        }
        self.generate_world_map()
        self.generate_battle_map()

    def generate_world_map(self):
        self.tile_map_world = [
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 21, 21, 21, 21, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 10, 10, 10, 57, 32, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 11, 36, 22, 22, 10, 10, 10, 10, 10, 10],
            [10, 21, 21, 21, 21, 10, 10, 10, 10, 31, 10, 32, 10, 10, 10, 10, 10, 10, 10, 10],

            [31, 10, 10, 10, 10, 33, 21, 21, 21, 34, 10, 33, 21, 21, 21, 21, 21, 21, 21, 10],
            [31, 10, 10, 10, 10, 10, 10, 13, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 32],
            [31, 10, 14, 10, 10, 69, 10, 13, 10, 10, 10, 10, 10, 10, 11, 10, 69, 10, 13, 32],
            [31, 10, 10, 10, 10, 36, 22, 22, 22, 35, 10, 10, 10, 10, 10, 12, 12, 12, 10, 32],

            [10, 22, 22, 22, 22, 10, 10, 10, 10, 31, 10, 10, 10, 10, 10, 10, 10, 10, 10, 32],
            [11, 10, 10, 10, 10, 10, 10, 10, 10, 31, 10, 12, 10, 10, 10, 10, 10, 10, 10, 32],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 10, 10, 10, 10, 10, 10, 10, 12, 10, 32],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 22, 35, 10, 13, 10, 36, 22, 22, 22, 10],

            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 11, 10, 10, 32, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 13, 10, 10, 10, 10, 31, 10, 10, 10, 32, 10, 10, 10, 10],
            [10, 10, 10, 14, 10, 10, 10, 10, 10, 10, 10, 10, 35, 10, 36, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 10, 32, 10, 10, 10, 10, 10]
        ]

    def generate_battle_map(self):
        self.tile_map_battle = [
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],

            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],

            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        ]

    def draw_world_level(self, window, camera):
        for y, row in enumerate(self.tile_map_world):
            for x, tile_id in enumerate(row):
                tile = self.tiles[tile_id]
                window.blit(tile,
                            (x * self.tile_width - camera.camera_rect.x, y * self.tile_height - camera.camera_rect.y))

    def draw_battle_level(self, window):
        for y, row in enumerate(self.tile_map_battle):
            for x, tile_id in enumerate(row):
                tile = self.tiles[tile_id]
                window.blit(tile, (x * self.tile_width, y * self.tile_height))

    def get_enemies(self):
        enemies = []
        for y, row in enumerate(self.tile_map_world):
            for x, tile_id in enumerate(row):
                if tile_id == 69:
                    enemies.append(character_init_enemy(enemy_list[random.randint(1,2)], x * self.tile_width, y * self.tile_height, None))
        return enemies

    def get_chests(self):
        chests = []
        for y, row in enumerate(self.tile_map_world):
            for x, tile_id in enumerate(row):
                if tile_id == 57:
                    chests.append(Chest(x * self.tile_width, y * self.tile_height))
        return chests
