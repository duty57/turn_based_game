import time

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

    def draw_item(self, item, spawn_time, x, y):
        if item is not None and time.time() - spawn_time < 2:
            #draw frame then item
            resized_frame = pygame.transform.scale(UI.item_frame[item.rarity], (50, 50))
            resized_item = pygame.transform.scale(item.image, (48, 48))
            self.window.blit(resized_frame, (1180, 0))
            self.window.blit(resized_item, (1182, 2))

    def draw(self, objects, item, spawn_time, item_x, item_y):
        self.window.fill((114, 117, 27))
        self.draw_level()
        self.draw_ui()
        self.draw_item(item, spawn_time, item_x, item_y)

        for obj in objects:
            if obj.name == "Chest":
                obj_rect = obj.rect.move(-self.camera.camera_rect.x, -self.camera.camera_rect.y)  # Adjust for camera
                self.window.blit(obj.image, (obj_rect.x, obj_rect.y))  # Draw chest using the adjusted rect position
                pygame.draw.rect(self.window, (255, 0, 0), obj_rect, 1)
            else:
                obj_rect = obj.rect.move(-self.camera.camera_rect.x, -self.camera.camera_rect.y)  # Adjust for camera
                obj.controller.draw(self.window, adjusted_rect=obj_rect)
        pygame.display.update()
