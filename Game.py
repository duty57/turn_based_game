import pygame

from turn_based_game.LoadCharacters import character_init_enemy
from turn_based_game.Renderer import Renderer
from turn_based_game.Battle import Battle

from Enums import Initiative


class Game:

    def __init__(self):
        self.window = None
        self.renderer = Renderer()
        self.clock = pygame.time.Clock()
        self.objects = pygame.sprite.Group()
        self.main_character = None
        self.enemies = []
        self.is_in_battle = False
        self.battle = None

        self.camera = None
    def add_objects(self, objects):
        self.objects.add(objects)

    def add_enemies(self, enemies):
        self.enemies = enemies
        self.objects.add(enemies)

    def add_main_character(self, character):
        self.main_character = character
        self.objects.add(character)

    def add_characters(self, characters):
        self.characters = characters
        self.renderer.characters = characters

    def add_camera(self, camera):
        self.camera = camera
        self.renderer.set_camera(camera)

    def create_window(self, width, height, fullscreen=False):
        self.window =  pygame.display.set_mode((width, height), pygame.FULLSCREEN if fullscreen else 0, pygame.DOUBLEBUF)
        self.renderer.create_window(self.window, width, height, fullscreen)
    def get_collision_rect(self):
        collision_rect = []
        for row_index, row in enumerate(self.renderer.tilemap):
            for col_index, tile in enumerate(row):
                if tile > 20 and tile < 40:
                    collision_rect.append(pygame.Rect(col_index * self.renderer.tile_width, row_index * self.renderer.tile_height, self.renderer.tile_width, self.renderer.tile_height))
        return collision_rect

    def detect_collision(self, character):
        collided_objects = pygame.sprite.spritecollide(character, self.objects, False)
        for obj in collided_objects:
            if obj != character and character.finished_attack:
                obj.collide()
                print("Collided with object")
                self.start_battle(Initiative.player_initiative)
                character.is_hit = False


            elif obj != character and not character.attacking and character.finished_hit:
                print("Collided with object")
                self.start_battle(Initiative.enemy_initiative)
                character.is_hit = False


    def start_battle(self, initiative=Initiative.player_initiative):
        turn_order = []
        self.is_in_battle = True
        self.generate_enemy_team()

        #calculate turn order
        if initiative == Initiative.player_initiative:
            for character in self.renderer.characters:
                turn_order.append(character)
            for enemy in self.enemies:
                turn_order.append(enemy)
        else:
            for character in self.renderer.characters:
                turn_order.append(character)
            for enemy in self.enemies:
                turn_order.append(enemy)

        self.battle = Battle(self.window, self.renderer.characters, self.enemies, initiative, turn_order)
        self.battle.set_camera(self.camera)
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
                self.main_character.controller(pygame.key.get_pressed(),
                                               self.get_collision_rect())  # Character controller
                self.renderer.camera.update(self.main_character)  # Update camera position
                self.detect_collision(self.main_character)  # Detect collision
                for obj in self.objects:
                    if obj.enemy:
                        obj.controller()
                self.renderer.draw(objects=self.objects) # Draw objects

            else:
                self.battle.draw()
        pygame.quit()
