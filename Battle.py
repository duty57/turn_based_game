from time import sleep

import pygame
from Enums import Initiative, CharacterBattleState, CharacterState, SelectionMode
import copy
from turn_based_game.GameUI import GameUI as UI
from turn_based_game.Level import Level
from turn_based_game.BattleRenderer import BattleRenderer
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
        self.battle_renderer = BattleRenderer(window, self.level)

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
            character.controller.x = 600
            character.controller.y = 500 - 80 * i
            character.controller.battle_x = 600
            character.controller.battle_y = 500 - 80 * i
            character.rect.center = (character.controller.x, character.controller.y)
            character.controller.moving_right_direction = True
            character.controller.moving_left_direction = False
            character.controller.idling = True
            character.controller.in_battle = True

        # set enemy positions
        for i, enemy in enumerate(self.enemy_team):
            enemy.controller.x = 1000
            enemy.controller.y = 500 - 80 * i
            enemy.controller.battle_x = 1000
            enemy.controller.battle_y = 500 - 80 * i
            enemy.rect.center = (enemy.controller.x, enemy.controller.y)
            enemy.controller.moving_right_direction = False
            enemy.controller.moving_left_direction = True
            enemy.controller.idling = True
            enemy.controller.in_battle = True
            enemy.controller.attackFrameCount = 0
            enemy.controller.frameCount = 0
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


    # combat logic
    def attack(self, attacker, target):
        if self.space_key_pressed:
            attacker.go_to_enemy(target)

    def controler(self):

        if not (self.enemy_team_highlight and self.player_team_highlight):
            self.end()

        elif self.turn_order[(self.current_turn - 1) % len(
                self.turn_order)].controller.battle_state.value == CharacterBattleState.back_in_position.value \
                and self.turn_order[(self.current_turn - 1) % len(
            self.turn_order)].controller.previous_battle_state.value == CharacterBattleState.attacking.value:

            current_character = self.turn_order[(self.current_turn - 1) % len(self.turn_order)]
            if current_character.controller.target.controller.character_state.value >= CharacterState.dead.value:
                print(self.enemy_team)
                self.turn_order.remove(current_character.controller.target)
                self.enemy_team_highlight.remove(
                    current_character.controller.target) if current_character.controller.target.is_enemy() else self.player_team_highlight.remove(
                    current_character.controller.target)

            self.turn_order[(self.current_turn - 1) % len(self.turn_order)].controller.previous_battle_state = self.turn_order[
                (self.current_turn - 1) % len(self.turn_order)].controller.battle_state
            self.turn_order[(self.current_turn - 1) % len(self.turn_order)].controller.battle_state = CharacterBattleState.idle
            print("Character back in position")
            self.current_turn_ui = self.current_turn
            self.current_turn_ui %= len(self.turn_order)

        # send current character info via list

        if not self.turn_order[(self.current_turn - 1) % len(self.turn_order)].controller.in_action and not self.turn_order[
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
                self.turn_order[self.current_turn % len(self.turn_order)].controller.target = self.enemy_team_highlight[
                    self.selection_index % len(self.enemy_team_highlight)]
                self.turn_order[self.current_turn % len(self.turn_order)].controller.going_to_enemy = True
                self.turn_order[self.current_turn % len(self.turn_order)].controller.in_action = True
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
            (self.current_turn - 1) % len(self.turn_order)].controller.in_action:

            if self.player_team_highlight:
                self.turn_order[self.current_turn % len(self.turn_order)].controller.target = self.player_team_highlight[0]
                self.turn_order[self.current_turn % len(self.turn_order)].controller.going_to_enemy = True
                self.turn_order[self.current_turn % len(self.turn_order)].controller.in_action = True
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

        self.battle_renderer.draw(self.player_team, self.enemy_team, self.turn_order, self.current_turn_ui, self.a_key_pressed, self.d_key_pressed, self.enter_key_pressed, self.enemy_team_highlight, self.selection_index)

    def draw(self):
        self.controler()
# TODO: maybe move calculate_turn_order call to character death event
# TODO: implement enemy AI to attack player characters
# TODO: enemy hit animation not always working
