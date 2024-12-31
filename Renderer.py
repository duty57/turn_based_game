import pygame
#[10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

class Renderer:

    def __init__(self):
        self.window = None
        self.camera = None  # Camera reference

    def create_window(self, width:int, height:int, fullscreen:bool = False):
        pygame.init()
        self.window = pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else 0)

    def set_camera(self, camera):
        """Set the camera to adjust rendering offsets."""
        self.camera = camera
    def draw_level(self):
        tilemap = [
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 21, 21, 21, 21, 10, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 10, 10, 10, 10, 32, 10, 10, 10, 10, 10],
            [10, 10, 10, 10, 10, 10, 10, 10, 10, 31, 11, 36, 22, 22, 10, 10, 10, 10, 10, 10],
            [10, 21, 21, 21, 21, 10, 10, 10, 10, 31, 10, 32, 10, 10, 10, 10, 10, 10, 10, 10],

            [31, 10, 10, 10, 10, 33, 21, 21, 21, 34, 10, 33, 21, 21, 21, 21, 21, 21, 21, 10],
            [31, 10, 10, 10, 10, 10, 10, 13, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 32],
            [31, 10, 14, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 11, 10, 10, 10, 13, 32],
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
        tilemap_width = len(tilemap[0])
        tilemap_height = len(tilemap)
        tile_width = 64
        tile_height = 64

        #0-10 common tiles
        #11-20 tiles with flowers
        #21-30 horizontal walls
        #31-40 vertical walls
        #41-50 background tiles
        tiles = {
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
        }

        for y, row in enumerate(tilemap):
            for x, tile_id in enumerate(row):
                tile = tiles[tile_id]
                tile_rect = pygame.Rect(
                    x * tile_width - self.camera.camera_rect.x,  # Adjust for camera offset
                    y * tile_height - self.camera.camera_rect.y,
                    tile_width,
                    tile_height
                )
                self.window.blit(tile, tile_rect)


    def draw(self, objects: list):
        self.window.fill((114, 117, 27))
        self.draw_level()

        for obj in objects:
            obj_rect = obj.rect.move(-self.camera.camera_rect.x, -self.camera.camera_rect.y)  # Adjust for camera
            obj.draw(self.window, obj_rect)
        pygame.display.update()
