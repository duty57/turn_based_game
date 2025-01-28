import pygame

from turn_based_game.Actors.Actor import Actor


class Camera:
    def __init__(self, level_width: int, level_height: int, screen_width: int, screen_height: int):
        self.camera_rect = pygame.Rect(0, 0, screen_width, screen_height)
        self.level_width = level_width
        self.level_height = level_height
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, target: Actor):
        # Center the camera on the target
        self.camera_rect.center = target.rect.center

        # Clamp the camera position within the level bounds
        self.camera_rect.x = max(0, min(self.camera_rect.x, self.level_width - self.screen_width))
        self.camera_rect.y = max(0, min(self.camera_rect.y, self.level_height - self.screen_height))
