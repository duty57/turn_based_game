import pygame

from turn_based_game.LoadCharacters import character_init_enemy
from turn_based_game.World_Renderer import WorldRenderer
from turn_based_game.Battle import Battle

from Enums import Initiative

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

    def add_objects(self, objects):
        self.objects.add(objects)

    def add_enemies(self, enemies):
        self.enemies = enemies
        self.objects.add(enemies)

    def add_characters(self, characters):
        self.characters = characters
        self.main_character = characters[0]
        self.objects.add(self.main_character)
        self.renderer.characters = characters

    def add_camera(self, camera):
        self.camera = camera
        self.renderer.set_camera(camera)

    def add_level(self, level):
        self.level = level
        self.renderer.set_level(level)
    def create_window(self, width, height, fullscreen=False):
        self.window = pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else 0, pygame.DOUBLEBUF)
        self.renderer.create_window(self.window)

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
                obj.controller.collide()
                print("Collided with object")
                self.start_battle(Initiative.player_initiative)
                character.controller.is_hit = False

            elif obj != character and obj.is_enemy() and obj.controller.finished_attack:
                print("Collided with object")
                self.start_battle(Initiative.enemy_initiative)
                character.controller.is_hit = False

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

    def generate_enemy_team(self):
        skeleton = character_init_enemy('Skeleton', 0, 0, self.main_character)
        goblin = character_init_enemy('Goblin', 500, 360, self.main_character)
        self.enemies.append(skeleton)
        self.enemies.append(goblin)

    def run(self, width, height, fullscreen=False):
        self.create_window(width, height, fullscreen)
        running = True
        while running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not self.is_in_battle:
                self.main_character.play(window=self.window, collisions=self.get_collision_rect())  # Character controller
                self.renderer.camera.update(self.main_character)  # Update camera position
                self.detect_collision(self.main_character)  # Detect collision
                for obj in self.objects:
                    if obj.is_enemy():
                        obj.play(window=self.window, adjusted_rect=pygame.Rect(0, 0, 1280, 720))
                self.renderer.draw(objects=self.objects)  # Draw objects

            else:
                self.battle.draw()
        pygame.quit()
