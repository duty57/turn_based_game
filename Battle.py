from time import sleep

import pygame
from Enums import Initiative


class Battle:

    def __init__(self, window, player_team, enemy_team, initiative, turn_order=[]):

        self.window = window
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.turn_order = turn_order
        self.initiative = initiative
        self.can_run = False
        self.current_turn = 0
        self.current_character_index = 0

        # Key press booleans
        self.a_key_pressed = False
        self.d_key_pressed = False
        self.enter_key_pressed = False
        self.escape_key_pressed = False
        self.space_key_pressed = False

        self.up_key_pressed = False
        self.down_key_pressed = False

        # Key release booleans
        self.a_key_released = None
        self.d_key_released = None
        self.enter_key_released = True
        self.escape_key_released = None
        self.space_key_released = None

        self.up_key_released = None
        self.down_key_released = None

        self.camera = None

        self.selection_index = 0

        self.profile_frame = pygame.image.load('turn_based_game/assets/UI/Frames/Frame.png')
        self.profile_frame = pygame.transform.scale(self.profile_frame, (50, 50))
        self.health_bar_frame = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Frame.png')
        self.action_points_bar_frame = pygame.image.load(
            'turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Frame.png')
        self.list_image = pygame.transform.scale(pygame.image.load('turn_based_game/assets/UI/Lists/list_long.png'), (325, 522))
        self.character_highlight = pygame.transform.scale(pygame.image.load('turn_based_game/assets/VFX/Highlights/Character_highlight.png'), (48, 12))
        self.enemy_highlight = pygame.transform.scale(pygame.image.load('turn_based_game/assets/VFX/Highlights/Enemy_highlight.png'), (48, 12))
    def set_camera(self, camera):
        self.camera = camera

    def start(self):
        self.calculate_turn_order()
        sleep(0.5)

        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        text_value = "Alies have the initiative!" if self.initiative == Initiative.player_initiative else "Enemies have the initiative!"
        color = (0, 255, 0) if self.initiative == Initiative.player_initiative else (255, 0, 0)
        text = font.render(text_value, True, color)
        text_rect = text.get_rect(center=(640, 360))
        self.window.fill((0, 0, 0))
        self.window.blit(text, text_rect)
        pygame.display.update()

        #set up the battle elements
        self.enemy_highlight.set_alpha(128)
        self.character_highlight.set_alpha(128)

        # set character positions
        for i, character in enumerate(self.player_team):
            character.x = 600
            character.y = 500 - 80 * i
            character.battle_x = 600
            character.battle_y = 500 - 80 * i
            character.rect.center = (character.x, character.y)
            character.moving_right_direction = True
            character.moving_left_direction = False
            character.idling = True
            character.in_battle = True

        #set enemy positions
        for i, enemy in enumerate(self.enemy_team):
            enemy.x = 1000
            enemy.y = 500 - 80 * i
            enemy.battle_x = 1000
            enemy.battle_y = 500 - 80 * i
            enemy.rect.center = (enemy.x, enemy.y)
            enemy.moving_right_direction = False
            enemy.moving_left_direction = True
            enemy.idling = True
            enemy.in_battle = True
        print("Battle started", self.turn_order)
        sleep(0.5)

    def calculate_turn_order(self):
        pass

    def draw_background(self):
        tilemap = [
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

        tiles = {
            10: pygame.image.load('turn_based_game/assets/Map/Tiles/Map_Tile_1.png'),
        }

        for y, row in enumerate(tilemap):
            for x, tile in enumerate(row):
                self.window.blit(tiles[tile], (x * 64, y * 64))

    #combat logic
    def attack(self, attacker, target):
        if self.space_key_pressed:
            attacker.go_to_enemy(target)

    # draw ui elements

    def draw_characters(self):
        for i, character in enumerate(self.player_team):
            character_rect = pygame.Rect(character.x-15, character.y-20, 30, 40)  # Adjust for camera
            character.controller(pygame.key.get_pressed())
            character.draw(self.window, character_rect)

    def draw_enemies(self):
        for i, enemy in enumerate(self.enemy_team):
            enemy_rect = pygame.Rect(enemy.x-10, enemy.y-20, 30, 40)
            enemy.controller()
            enemy.draw(self.window, enemy_rect)

    def draw_characters_list(self):
        for i, character in enumerate(self.player_team):
            character.draw_ui(self.window, self.profile_frame, self.health_bar_frame, self.action_points_bar_frame,
                              85 * i + 25)

    def draw_enemy_list(self):
        for i, enemy in enumerate(self.enemy_team):
            enemy.draw_ui(self.window, self.profile_frame, self.health_bar_frame, self.action_points_bar_frame,
                          1220 - 85 * i)

    def draw_actions(self):
        a_key = pygame.image.load('turn_based_game/assets/UI/Keys/keyboard_key_a.png')
        d_key = pygame.image.load('turn_based_game/assets/UI/Keys/keyboard_key_d.png')

        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)

        item_text = font.render("Items", True, (255, 255, 255))
        skill_text = font.render("Skills", True, (255, 255, 255))

        self.window.blit(a_key, (15, 685))
        self.window.blit(item_text, (60, 690))
        self.window.blit(d_key, (150, 685))
        self.window.blit(skill_text, (195, 690))

    def draw_item_list(self):
        if self.a_key_pressed:
            font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
            self.window.blit(self.list_image, (15, 100))
            text = font.render("Items", True, (255, 255, 255))
            self.window.blit(text, (140, 75))

    def draw_skill_list(self):
        if self.d_key_pressed:
            font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
            self.window.blit(self.list_image, (15, 100))
            text = font.render("Skills", True, (255, 255, 255))
            self.window.blit(text, (140, 75))

    def draw_highlight(self):
        if self.enter_key_pressed:
            # if self.player_team[self.current_character_index].character_class == 'Healer':
            #     self.selection_index = len(self.player_team)-1 if self.selection_index > len(self.player_team)-1 else (0 if self.selection_index < 0 else self.selection_index)
            #     self.window.blit(self.character_highlight, (600-24, 500 + 8 - 80 * self.selection_index))
            # else:
                self.selection_index = len(self.enemy_team)-1 if self.selection_index > len(self.enemy_team)-1 else (0 if self.selection_index < 0 else self.selection_index)
                self.window.blit(self.enemy_highlight, (1000 - 24, 500 - 80 * self.selection_index))
    def controler(self):
        if not self.player_team[(self.current_character_index-1) % len(self.player_team)].in_action:
            keys = pygame.key.get_pressed()
            # Handle items key toggling
            if keys[pygame.K_a] and self.a_key_released:
                self.a_key_pressed = not self.a_key_pressed
                self.d_key_pressed = False
                self.a_key_released = False
            elif not keys[pygame.K_a]:
                self.a_key_released = True
            # Handle skills key toggling
            if keys[pygame.K_d] and self.d_key_released:
                self.d_key_pressed = not self.d_key_pressed
                self.a_key_pressed = False
                self.d_key_released = False
            elif not keys[pygame.K_d]:
                self.d_key_released = True

            # Common attack key toggling
            if keys[pygame.K_RETURN] and self.enter_key_released:
                print("Enter key pressed")
                self.enter_key_pressed = not self.enter_key_pressed
                self.enter_key_released = False

            # Back key toggling
            if keys[pygame.K_ESCAPE]:
                self.a_key_pressed = False
                self.d_key_pressed = False
                self.enter_key_pressed = False
                self.enter_key_released = True

            if keys[pygame.K_UP] and self.up_key_released and self.enter_key_pressed:
                self.selection_index += 1
                self.up_key_released = False
            elif not keys[pygame.K_UP]:
                self.up_key_released = True

            if keys[pygame.K_DOWN] and self.down_key_released and self.enter_key_pressed:
                self.selection_index -= 1
                self.down_key_released = False
            elif not keys[pygame.K_DOWN]:
                self.down_key_released = True

            if keys[pygame.K_SPACE] and self.enter_key_pressed and self.space_key_released:
                self.space_key_pressed = True
                self.space_key_released = False
                self.enter_key_pressed = False
                self.enter_key_released = True
                self.player_team[self.current_character_index].target = self.enemy_team[self.selection_index]
                self.player_team[self.current_character_index].going_to_enemy = True
                self.player_team[self.current_character_index].in_action = True
                self.current_character_index += 1
                self.current_character_index %= len(self.player_team)
            elif not keys[pygame.K_SPACE]:
                self.space_key_released = True

    def draw(self):
        self.window.fill((255, 255, 255))
        self.draw_background()
        self.draw_characters_list()
        self.draw_characters()
        self.draw_enemies()
        self.draw_enemy_list()
        self.draw_actions()
        self.controler()
        self.draw_item_list()
        self.draw_skill_list()
        self.draw_highlight()

        pygame.display.update()

    def render(self):
        pass

    def update(self):
        pass

#TODO: maybe add offset for the highlight of specific character
#TODO: skeleton hit animation not working