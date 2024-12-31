import pygame

from turn_based_game.Renderer import Renderer


class Game:

    def __init__(self):
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.objects = pygame.sprite.Group()
        self.main_character = None

    def add_objects(self, objects):
        self.objects.add(objects)

    def add_main_character(self, character):
        self.main_character = character
        self.objects.add(character)

    def add_camera(self, camera):
        self.renderer.set_camera(camera)

    def detect_collision(self, character):
        collided_objects = pygame.sprite.spritecollide(character, self.objects, False)
        for obj in collided_objects:
            if obj != character and character.attacking:
                obj.collide()

    def run(self, width, height, fullscreen=False):
        self.renderer.create_window(width, height, fullscreen)
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.main_character.controller(pygame.key.get_pressed()) # Character controller
            self.renderer.camera.update(self.main_character) # Update camera position
            for obj in self.objects:
                if obj.enemy:
                    obj.controller()
            self.detect_collision(self.main_character) # Detect collision with other objects
            self.renderer.draw(objects=self.objects)

        pygame.quit()
