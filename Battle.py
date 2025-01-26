from time import sleep

import pygame
from Enums import Initiative, CharacterBattleState, CharacterState, SelectionMode
import copy
from turn_based_game.GameUI import GameUI as UI
from turn_based_game.Level import Level
from turn_based_game.BattleRenderer import BattleRenderer
from turn_based_game.BattleRenderer import draw_message

pygame.mixer.init()
ambient_music = pygame.mixer.Sound('turn_based_game/audio/ambient_battle.mp3')

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
        self.initiative = initiative  # player_initiative or enemy_initiative

        # Turn order variables
        self.current_turn = 0
        self.current_turn_ui = 0
        self.current_character_index = 0
        self.first_cycle = True

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

        # Selection variables
        self.selection_mode = SelectionMode.enemy
        self.selection_index = 0
        self.skill_selection_index = 0
        self.item_selection_index = 0

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
            character.controller.battle_start(i)

        # set enemy positions
        for i, enemy in enumerate(self.enemy_team):
            enemy.controller.battle_start(i)
        sleep(0.5)
        # ambient_music.play(10)
        # ambient_music.set_volume(0.1)

    def end(self):
        sleep(0.5)
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        if self.enemy_team_highlight:
            text_value = "GAME OVER!"
            color = (255, 0, 0)
            text = font.render(text_value, True, color)
            text_rect = text.get_rect(center=(640, 360))
            self.window.fill((0, 0, 0))
            self.window.blit(text, text_rect)
            pygame.display.update()
            sleep(0.5)
            pygame.quit()
            exit()
        else:
            text_value = "VICTORY!"
            color = (0, 255, 0)
            text = font.render(text_value, True, color)
            text_rect = text.get_rect(center=(640, 360))
            self.window.fill((0, 0, 0))
            self.window.blit(text, text_rect)
            pygame.display.update()
            for character in self.player_team:
                character.gain_experience(50)
                character.controller.end_of_battle()
            sleep(0.5)

    def calculate_turn_order(self):
        self.turn_order.sort(key=lambda x: x.speed, reverse=True)

    # combat logic
    def attack(self, attacker, target):
        if self.space_key_pressed:
            attacker.go_to_enemy(target)

    # TODO create 3 paths: common attack, item, skill (select, use, back)
    def controler(self):

        previous_character = self.turn_order[(self.current_turn - 1) % len(self.turn_order)]
        current_character_controller = self.turn_order[self.current_turn % len(self.turn_order)].controller
        if not (self.enemy_team_highlight and self.player_team_highlight):  # if one of the teams is empty
            self.end()

        elif previous_character.controller.battle_state.value == CharacterBattleState.back_in_position.value \
                and previous_character.controller.previous_battle_state.value == CharacterBattleState.attacking.value:

            for actor in self.turn_order:
                if actor.controller.character_state.value >= CharacterState.dead.value:
                    self.turn_order.remove(actor)
                    if actor in self.player_team_highlight:
                        self.player_team_highlight.remove(actor)
                    elif actor in self.enemy_team_highlight:
                        self.enemy_team_highlight.remove(actor)

            previous_character.controller.previous_battle_state = self.turn_order[
                (self.current_turn - 1) % len(self.turn_order)].controller.battle_state
            previous_character.controller.battle_state = CharacterBattleState.idle
            self.current_turn_ui = self.current_turn
            self.current_turn_ui %= len(self.turn_order)

        # send current character info via list

        if not previous_character.controller.in_action and not current_character_controller.actor.is_enemy():

            keys = pygame.key.get_pressed()
            # Handle items key toggling
            if keys[pygame.K_a] and self.a_key_released:  # open items
                self.a_key_pressed = not self.a_key_pressed
                self.d_key_pressed = False
                self.a_key_released = False
            elif not keys[pygame.K_a]:
                self.a_key_released = True
            # Handle skills key toggling
            if keys[pygame.K_d] and self.d_key_released:  # open skills
                self.d_key_pressed = not self.d_key_pressed
                self.a_key_pressed = False
                self.d_key_released = False
            elif not keys[pygame.K_d]:
                self.d_key_released = True

            # Common attack key toggling
            if keys[pygame.K_RETURN] and self.enter_key_released:  # attack
                self.enter_key_pressed = not self.enter_key_pressed
                self.enter_key_released = False

                if self.a_key_pressed:
                    print("Item selected")
                elif self.d_key_pressed:
                    skill = current_character_controller.actor.skills[
                        self.skill_selection_index % len(current_character_controller.actor.skills)]
                    current_character_controller.is_skill_selected = True

            # Back key toggling
            if keys[pygame.K_ESCAPE]:  # back
                self.a_key_pressed = False
                self.d_key_pressed = False
                self.enter_key_pressed = False
                self.enter_key_released = True
                current_character_controller.is_skill_selected = False

            if keys[pygame.K_UP] and self.up_key_released:  # select target
                if self.d_key_pressed and self.enter_key_released:
                    self.skill_selection_index += 1
                elif self.a_key_pressed and self.enter_key_released:
                    self.item_selection_index += 1
                elif self.enter_key_pressed:
                    self.selection_index += 1

                self.up_key_released = False
            elif not keys[pygame.K_UP]:
                self.up_key_released = True

            if keys[pygame.K_DOWN] and self.down_key_released:  # select target
                if self.d_key_pressed and self.enter_key_released:
                    self.skill_selection_index -= 1
                elif self.a_key_pressed and self.enter_key_released:
                    self.item_selection_index -= 1
                elif self.enter_key_pressed:
                    self.selection_index -= 1
                self.down_key_released = False
            elif not keys[pygame.K_DOWN]:
                self.down_key_released = True

            if keys[pygame.K_SPACE] and self.enter_key_pressed and self.space_key_released:  # accept target
                self.space_key_pressed = True
                self.space_key_released = False
                self.enter_key_pressed = False
                self.enter_key_released = True

                skill = current_character_controller.actor.skills[
                    self.skill_selection_index % len(current_character_controller.actor.skills)]

                if current_character_controller.is_skill_selected:
                    if skill['type'] == 'attack':
                        current_character_controller.target = self.enemy_team_highlight[
                            self.selection_index % len(self.enemy_team_highlight)]
                        if current_character_controller.actor.action_points >= skill['cost']:
                            current_character_controller.attack_skill(skill, enemy_team=self.enemy_team_highlight)
                            self.current_turn = (self.current_turn + 1) % len(self.turn_order)
                        else:
                            draw_message(self.window, "Not enough action points", (current_character_controller.x, current_character_controller.y))
                            self.escape_key_pressed = True
                        current_character_controller.is_skill_selected = False
                    else:
                        if skill['targets'] == 'self':
                            self.skill_selection_index = self.player_team_highlight.index(
                                current_character_controller.actor)
                            current_character_controller.target = current_character_controller.actor
                        else:
                            current_character_controller.target = self.player_team_highlight[
                                self.selection_index % len(self.player_team_highlight)]
                        if current_character_controller.actor.action_points >= skill['cost']:
                            current_character_controller.healing_skill(skill, player_team=self.player_team)
                            self.current_turn = (self.current_turn + 1) % len(self.turn_order)
                        else:
                            draw_message(self.window, "Not enough action points", 2)
                            self.escape_key_pressed = True
                        current_character_controller.is_skill_selected = False
                else:
                    current_character_controller.target = self.enemy_team_highlight[
                        self.selection_index % len(self.enemy_team_highlight)]
                    current_character_controller.going_to_enemy = True
                    current_character_controller.in_action = True
                    self.current_turn = (self.current_turn + 1) % len(self.turn_order)

                if not self.first_cycle:
                    previous_character = self.turn_order[self.current_turn - 1]
                    current_character_controller = self.turn_order[self.current_turn % len(self.turn_order)].controller
                    # self.calculate_turn_order()
                    self.current_turn = self.turn_order.index(previous_character) + 1
                    self.current_turn %= len(self.turn_order)

                self.a_key_pressed = False
                self.d_key_pressed = False
                self.enter_key_pressed = False
            elif not keys[pygame.K_SPACE]:
                self.space_key_released = True

        elif current_character_controller.actor.is_enemy() and not previous_character.controller.in_action:

            if self.player_team_highlight:
                current_character_controller.target = current_character_controller.enemy_to_attack(self.player_team_highlight)
                if current_character_controller.is_skill_selected:
                    current_character_controller.attack_skill(self.player_team_highlight)
                else:
                    current_character_controller.going_to_enemy = True
                    current_character_controller.in_action = True
                current_character_controller.is_skill_selected = False
                self.current_turn += 1
                self.current_turn %= len(self.turn_order)


            if not self.first_cycle:
                previous_character = self.turn_order[self.current_turn - 1]
                current_character_controller = self.turn_order[self.current_turn % len(self.turn_order)].controller
                # self.calculate_turn_order()
                self.current_turn = self.turn_order.index(previous_character) + 1
                self.current_turn %= len(self.turn_order)

        if self.current_turn_ui == len(self.turn_order) - 1:
            self.first_cycle = False
        is_attack = True
        if not current_character_controller.actor.is_enemy():
            skill = current_character_controller.actor.skills[
                self.skill_selection_index % len(current_character_controller.actor.skills)]
            is_attack = skill['type'] == 'attack' if current_character_controller.is_skill_selected else True
        self.battle_renderer.draw(self.player_team, self.enemy_team, self.turn_order, self.current_turn_ui,
                                  self.a_key_pressed, self.d_key_pressed, self.enter_key_pressed,
                                  self.enemy_team_highlight, self.player_team_highlight, self.selection_index,
                                  self.skill_selection_index, self.item_selection_index, is_attack)

    def draw(self):
        self.controler()
# TODO: implement enemy AI to attack player characters
# TODO: order calculation could be broken

#TODO: immunities and weaknesses breaks after first cycle