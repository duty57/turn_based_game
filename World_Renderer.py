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

    def draw_item(self, item, spawn_time):
        if item is not None and time.time() - spawn_time < 2:
            #draw frame then item
            resized_frame = pygame.transform.scale(UI.item_frame[item.rarity], (50, 50))
            resized_item = pygame.transform.scale(item.image, (48, 48))
            self.window.blit(resized_frame, (1180, 0))
            self.window.blit(resized_item, (1182, 2))

    def draw_inventory(self, inventory, character_index, selection_index):
        self.window.fill((114, 117, 27))
        self.draw_level()
        self.draw_ui()

        alpha_surface = pygame.Surface(self.window.get_size(), pygame.SRCALPHA)
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
        inventory_text = font.render("Inventory", True, (255, 255, 255))
        character_text = font.render(self.characters[character_index % len(self.characters)].name, True, (255, 255, 255))

        alpha_surface.fill((0, 0, 0, 128)) # Fill the surface with a transparent black color
        self.window.blit(alpha_surface, (0, 0))

        self.window.blit(inventory_text, (1030, 75))
        self.window.blit(UI.list_image, (930, 100))
        adj_rect = pygame.Rect(800, 125, 300, 500)
        self.window.blit(character_text, (775, 75))
        self.characters[character_index % len(self.characters)].controller.draw(self.window, adj_rect)

        for i, item in enumerate(inventory):
            if i == selection_index % len(inventory):
                pygame.draw.rect(self.window, (255, 0, 0), (960, 125 + 50 * i, 265, 50), 1)
            self.window.blit(item.image, (960, 125 + 50 * i))
            font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 16)
            item_name_text = font.render(item.name, True, (255, 255, 255))
            item_stats_text = font.render(item.get_stats(), True, (255, 255, 0))
            self.window.blit(item_name_text, (1015, 125 + 50 * i))
            self.window.blit(item_stats_text, (1010, 150 + 50 * i))

        pygame.display.update()

    def draw(self, objects, item, spawn_time):
        self.window.fill((114, 117, 27))
        self.draw_level()
        self.draw_ui()
        self.draw_item(item, spawn_time)

        for obj in objects:
            if obj.name == "Chest":
                obj_rect = obj.rect.move(-self.camera.camera_rect.x, -self.camera.camera_rect.y)  # Adjust for camera
                self.window.blit(obj.image, (obj_rect.x, obj_rect.y))  # Draw chest using the adjusted rect position
                pygame.draw.rect(self.window, (255, 0, 0), obj_rect, 1)
            else:
                obj_rect = obj.rect.move(-self.camera.camera_rect.x, -self.camera.camera_rect.y)  # Adjust for camera
                obj.controller.draw(self.window, adjusted_rect=obj_rect)

        pygame.display.update()
