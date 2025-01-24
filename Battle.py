from time import sleep

import pygame
from Enums import Initiative, CharacterBattleState, CharacterState, SelectionMode
import copy
from turn_based_game.GameUI import GameUI as UI
from turn_based_game.Level import Level

class Battle:

    def __init__(self, window: pygame.Surface, player_team: list, enemy_team: list, initiative: Initiative,
                 turn_order: list = None):

        if turn_order is None:
            turn_order = []
        self.window = window
        self.player_team = player_team
        self.enemy_team = enemy_team
        self.turn_order = turn_order
        self.player_team_highlight = copy.copy(player_team)
        self.enemy_team_highlight = copy.copy(enemy_team)
        self.initiative = initiative
        self.current_turn = 0
        self.current_turn_ui = 0
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

        self.selection_mode = SelectionMode.enemy
        self.selection_index = 0

        self.first_cycle = True
        self.level = Level()

    def start(self):
        sleep(0.5)

        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        text_value = "Alies have the initiative!" if self.initiative == Initiative.player_initiative else "Enemies have the initiative!"
        color = (0, 255, 0) if self.initiative == Initiative.player_initiative else (255, 0, 0)
        text = font.render(text_value, True, color)
        text_rect = text.get_rect(center=(640, 360))
        self.window.fill((0, 0, 0))
        self.window.blit(text, text_rect)
        pygame.display.update()

        # set up the battle elements
        UI.enemy_highlight.set_alpha(128)
        UI.character_highlight.set_alpha(128)

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

        # set enemy positions
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
            enemy.attackFrameCount = 0
            enemy.frameCount = 0
        sleep(0.5)

    def end(self):
        sleep(0.5)
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        text_value = "VICTORY!" if not self.enemy_team_highlight else "GAME OVER!"
        color = (0, 255, 0) if not self.enemy_team_highlight else (255, 0, 0)
        text = font.render(text_value, True, color)
        text_rect = text.get_rect(center=(640, 360))
        self.window.fill((0, 0, 0))
        self.window.blit(text, text_rect)
        pygame.display.update()
        sleep(0.5)

    def calculate_turn_order(self):
        self.turn_order.sort(key=lambda x: x.speed, reverse=True)

    def draw_background(self):
        self.level.draw_battle_level(self.window)

    # combat logic
    def attack(self, attacker, target):
        if self.space_key_pressed:
            attacker.go_to_enemy(target)

    # draw ui elements

    def draw_characters(self):
        for i, character in enumerate(self.player_team):
            character_rect = pygame.Rect(character.x - 15, character.y - 20, 30, 40)  # Adjust for camera
            character.controller(pygame.key.get_pressed())
            character.draw(self.window, character_rect)

    def draw_enemies(self):
        for i, enemy in enumerate(self.enemy_team):
            enemy_rect = pygame.Rect(enemy.x - 10, enemy.y - 20, 30, 40)
            enemy.controller()
            enemy.draw(self.window, enemy_rect)

    def draw_characters_list(self):
        for i, character in enumerate(self.player_team):
            character.draw_ui(self.window, UI.profile_frame, UI.death_frame, UI.health_bar_frame,
                              UI.action_points_bar_frame,
                              85 * i + 25)

    def draw_enemy_list(self):
        for i, enemy in enumerate(self.enemy_team):
            enemy.draw_ui(self.window, UI.profile_frame, UI.death_frame, UI.health_bar_frame,
                          UI.action_points_bar_frame,
                          1220 - 85 * i)

    def draw_actions(self):

        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)

        item_text = font.render("Items", True, (182, 182, 182))
        skill_text = font.render("Skills", True, (182, 182, 182))
        select_text = font.render("Select", True, (182, 182, 182))
        use_text = font.render("Use", True, (182, 182, 182))

        self.window.blit(UI.a_key, (15, 685))
        self.window.blit(item_text, (60, 690))
        self.window.blit(UI.d_key, (165, 685))
        self.window.blit(skill_text, (210, 690))
        self.window.blit(UI.enter_key, (340, 685))
        self.window.blit(select_text, (385, 690))
        self.window.blit(UI.space_key, (510, 685))
        self.window.blit(use_text, (590, 690))

    def draw_item_list(self):
        if self.a_key_pressed:
            font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
            self.window.blit(UI.list_image, (15, 100))
            text = font.render("Items", True, (255, 255, 255))
            self.window.blit(text, (140, 75))

    def draw_skill_list(self):
        if self.d_key_pressed:
            font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
            self.window.blit(UI.list_image, (15, 100))
            text = font.render("Skills", True, (255, 255, 255))
            self.window.blit(text, (140, 75))
            for i, skill in enumerate(self.turn_order[self.current_turn].skills):
                font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 16)
                rect = pygame.Rect(50, 125 + 67 * i, 255, 65)
                pygame.draw.rect(self.window, (0, 0, 0), rect, 2)

                skill_text = font.render(skill['name'] + ':', True, (255, 255, 255))
                self.window.blit(skill_text, (55, 130 + 67 * i))

                skill_text = font.render(str(skill['cost']), True, (255, 255, 0))
                self.window.blit(skill_text, (180, 130 + 67 * i))

                font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 12)
                for j, line in enumerate(skill['description'].split('\n')):
                    skill_text = font.render(line, True, (255, 255, 255))
                    self.window.blit(skill_text, (55, 150 + 67 * i + 12 * j))

    def draw_highlight(self):
        if self.enter_key_pressed:
            # if self.player_team[self.current_character_index].character_class == 'Witch':
            #     self.selection_index = len(self.player_team)-1 if self.selection_index > len(self.player_team)-1 else (0 if self.selection_index < 0 else self.selection_index)
            #     self.window.blit(self.character_highlight, (600-24, 500 + 8 - 80 * self.selection_index))
            # else:
            #     self.selection_index = self.enemy_team.index(self.enemy_team_highlight[len(self.enemy_team_highlight)-1]) if self.selection_index > len(self.enemy_team_highlight)-1\
            #         else (0 if self.enemy_team.index(self.enemy_team_highlight[self.selection_index]) < 0 else self.enemy_team.index(self.enemy_team_highlight[self.selection_index]))
            self.window.blit(UI.enemy_highlight, (1000 - 24, 500 + 5 - 80 * self.enemy_team.index(
                self.enemy_team_highlight[self.selection_index % len(self.enemy_team_highlight)])))
            self.window.blit(UI.enemy_frame_highlight, (1220 - 85 * self.enemy_team.index(
                self.enemy_team_highlight[self.selection_index % len(self.enemy_team_highlight)]), 0))

    def draw_turn_order(self):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 16)
        text_now = font.render("Now", True, (255, 255, 0))
        text_next = font.render("Next", True, (255, 255, 0))
        if self.turn_order[self.current_turn_ui % len(self.turn_order)].is_enemy():
            self.window.blit(text_now, (
                1223 - 85 * self.enemy_team.index(self.turn_order[self.current_turn_ui % len(self.turn_order)]), 2))
        else:
            self.window.blit(text_now, (
                28 + 85 * self.player_team.index(self.turn_order[self.current_turn_ui % len(self.turn_order)]), 2))

        if self.turn_order[(self.current_turn_ui + 1) % len(self.turn_order)].is_enemy():
            self.window.blit(text_next, (
                1223 - 85 * self.enemy_team.index(self.turn_order[(self.current_turn_ui + 1) % len(self.turn_order)]),
                2))
        else:
            self.window.blit(text_next, (
                28 + 85 * self.player_team.index(self.turn_order[(self.current_turn_ui + 1) % len(self.turn_order)]),
                2))

    def controler(self):

        if not (self.enemy_team_highlight and self.player_team_highlight):
            self.end()

        elif self.turn_order[(self.current_turn - 1) % len(
                self.turn_order)].battle_state.value == CharacterBattleState.back_in_position.value \
                and self.turn_order[(self.current_turn - 1) % len(
            self.turn_order)].previous_battle_state.value == CharacterBattleState.attacking.value:

            current_character = self.turn_order[(self.current_turn - 1) % len(self.turn_order)]
            if current_character.target.character_state.value >= CharacterState.dead.value:
                print(self.enemy_team)
                self.turn_order.remove(current_character.target)
                self.enemy_team_highlight.remove(
                    current_character.target) if current_character.target.is_enemy() else self.player_team_highlight.remove(
                    current_character.target)

            self.turn_order[(self.current_turn - 1) % len(self.turn_order)].previous_battle_state = self.turn_order[
                (self.current_turn - 1) % len(self.turn_order)].battle_state
            self.turn_order[(self.current_turn - 1) % len(self.turn_order)].battle_state = CharacterBattleState.idle
            print("Character back in position")
            self.current_turn_ui = self.current_turn
            self.current_turn_ui %= len(self.turn_order)

        # send current character info via list

        if not self.turn_order[(self.current_turn - 1) % len(self.turn_order)].in_action and not self.turn_order[
            self.current_turn % len(self.turn_order)].is_enemy():

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
                self.turn_order[self.current_turn % len(self.turn_order)].target = self.enemy_team_highlight[
                    self.selection_index % len(self.enemy_team_highlight)]
                self.turn_order[self.current_turn % len(self.turn_order)].going_to_enemy = True
                self.turn_order[self.current_turn % len(self.turn_order)].in_action = True
                self.current_turn += 1
                self.current_turn %= len(self.turn_order)

                if not self.first_cycle:
                    print("Calculating turn order")
                    current_character = self.turn_order[self.current_turn - 1]
                    self.calculate_turn_order()
                    print(self.turn_order)
                    self.current_turn = self.turn_order.index(current_character) + 1
                    self.current_turn %= len(self.turn_order)
            elif not keys[pygame.K_SPACE]:
                self.space_key_released = True

        elif self.turn_order[self.current_turn % len(self.turn_order)].is_enemy() and not self.turn_order[
            (self.current_turn - 1) % len(self.turn_order)].in_action:

            if self.player_team_highlight:
                self.turn_order[self.current_turn % len(self.turn_order)].target = self.player_team_highlight[0]
                self.turn_order[self.current_turn % len(self.turn_order)].going_to_enemy = True
                self.turn_order[self.current_turn % len(self.turn_order)].in_action = True
                self.current_turn += 1
                self.current_turn %= len(self.turn_order)

            if not self.first_cycle:
                print("Calculating turn order")
                current_character = self.turn_order[self.current_turn - 1]
                self.calculate_turn_order()
                print(self.turn_order)
                self.current_turn = self.turn_order.index(current_character) + 1
                self.current_turn %= len(self.turn_order)

        if self.current_turn_ui == len(self.turn_order) - 1:
            self.first_cycle = False

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
        self.draw_turn_order()
        pygame.display.update()

    def render(self):
        pass

    def update(self):
        pass

# TODO: maybe move calculate_turn_order call to character death event
# TODO: implement enemy AI to attack player characters
# TODO: enemy hit animation not always working
