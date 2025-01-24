import pygame
from turn_based_game.GameUI import GameUI as UI
from turn_based_game.Level import Level


# [10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

class WorldRenderer:

    def __init__(self):
        self.window = None
        self.camera = None  # Camera reference
        self.characters = []  # 1) main character 2) wizard 3) healer 4) archer
        self.level = None

    def create_window(self, window):
        pygame.init()
        self.window = window

    def set_camera(self, camera):
        """Set the camera to adjust rendering offsets."""
        self.camera = camera

    def set_level(self, level: Level):
        self.level = level

    def draw_level(self):
        self.level.draw_world_level(self.window, self.camera)

    def draw_ui(self):
        self.window.blit(UI.profile_frame, (1230, 0))
        self.window.blit(UI.backpack, (1230, -7))
        for i, character in enumerate(self.characters):
            character.controller.draw_ui(self.window, UI.profile_frame, UI.death_frame, UI.health_bar_frame,
                              UI.action_points_bar_frame,
                              85 * i + 25)

    def draw(self, objects: list):
        self.window.fill((114, 117, 27))
        self.draw_level()
        self.draw_ui()

        for obj in objects:
            obj_rect = obj.rect.move(-self.camera.camera_rect.x, -self.camera.camera_rect.y)  # Adjust for camera
            obj.controller.draw(self.window, adjusted_rect=obj_rect)
        pygame.display.update()
