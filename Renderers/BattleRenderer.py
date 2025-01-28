import pygame

from turn_based_game.Enums import Initiative
from turn_based_game.Dataclasses.GameUI import GameUI as UI, draw_ui


def draw_message(window, message, position, duration=1000):
    if not isinstance(position, tuple):
        raise TypeError("Position must be a tuple containing x and y coordinates")
    font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 14)
    text = font.render(message, True, (255, 0, 0))
    window.blit(text, (position[0] + 50, position[1] - 25))
    pygame.display.update()
    pygame.time.delay(duration)

class BattleRenderer:

    def __init__(self, window, level):
        self.window = window
        self.level = level

    def start(self, initiative):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        text_value = "Alies have the initiative!" if initiative.value == Initiative.player_initiative.value else "Enemies have the initiative!"
        color = (0, 255, 0) if initiative.value == Initiative.player_initiative.value else (255, 0, 0)
        text = font.render(text_value, True, color)
        text_rect = text.get_rect(center=(640, 360))
        self.window.fill((0, 0, 0))
        self.window.blit(text, text_rect)
        pygame.display.update()
        # set up the battle elements
        UI.enemy_highlight.set_alpha(128)
        UI.character_highlight.set_alpha(128)

    def end(self, text_value: str, color: tuple):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        text = font.render(text_value, True, color)
        text_rect = text.get_rect(center=(640, 360))
        self.window.fill((0, 0, 0))
        self.window.blit(text, text_rect)
        pygame.display.update()

    def set_level(self, level):
        self.level = level

    # draw ui elements
    def draw_background(self):
        self.level.draw_battle_level(self.window)

    def draw_characters(self, player_team):
        for i, character in enumerate(player_team):
            character_rect = pygame.Rect(character.controller.x - 15, character.controller.y - 20, 30,
                                         40)  # Adjust for camera
            character.play(self.window, character_rect)

    def draw_enemies(self, enemy_team):
        for i, enemy in enumerate(enemy_team):
            if enemy.name == "Flying Demon":
                enemy_rect = pygame.Rect(enemy.controller.x - 20, enemy.controller.y - 40, 30, 40)
            else:
                enemy_rect = pygame.Rect(enemy.controller.x - 10, enemy.controller.y - 20, 30, 40)
            enemy.play(self.window, enemy_rect)

    def draw_characters_list(self, player_team):
        for i, character in enumerate(player_team):
            draw_ui(self.window, character, 85 * i + 25)

    def draw_enemy_list(self, enemy_team):
        for i, enemy in enumerate(enemy_team):
            draw_ui(self.window, enemy, 1220 - 85 * i)

    def draw_level_up(self, characters):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 48)
        text = font.render("LEVEL UP!", True, (255, 255, 0))
        text_rect = text.get_rect(center=(self.window.get_width() // 2, 50))
        self.window.fill((0, 0, 0))
        self.window.blit(text, text_rect)

        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
        for i, character in enumerate(characters):
            name_text = font.render(character.name, True, (255, 255, 255))
            self.window.blit(name_text, (150 + 300 * i, 450))

            prev_hp_text = font.render(f"HP: {character.max_health - 10}=>", True, (255, 255, 255))
            prev_ap_text = font.render(f"AP: {character.max_action_points - 5}=>", True, (255, 255, 255))
            prev_atk_text = font.render(f"ATK: {character.strength - 1}=>", True, (255, 255, 255))
            prev_def_text = font.render(f"DEF: {character.defense - 1}=>", True, (255, 255, 255))

            new_hp_text = font.render(f"HP: {character.max_health}", True, (255, 255, 0))
            new_ap_text = font.render(f"AP: {character.max_action_points}", True, (255, 255, 0))
            new_atk_text = font.render(f"ATK: {character.strength}", True, (255, 255, 0))
            new_def_text = font.render(f"DEF: {character.defense}", True, (255, 255, 0))

            self.window.blit(prev_hp_text, (100 + 300 * i, 500))
            self.window.blit(prev_ap_text, (100 + 300 * i, 530))
            self.window.blit(prev_atk_text, (100 + 300 * i, 560))
            self.window.blit(prev_def_text, (100 + 300 * i, 590))

            self.window.blit(new_hp_text, (205 + 300 * i, 500))
            self.window.blit(new_ap_text, (205 + 300 * i, 530))
            self.window.blit(new_atk_text, (205 + 300 * i, 560))
            self.window.blit(new_def_text, (205 + 300 * i, 590))

        pygame.display.update()

    def draw_actions(self):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
        skill_text = font.render("Skills", True, (182, 182, 182))
        select_text = font.render("Select", True, (182, 182, 182))
        use_text = font.render("Use", True, (182, 182, 182))

        self.window.blit(UI.d_key, (15, 685))
        self.window.blit(skill_text, (60, 690))
        self.window.blit(UI.enter_key, (190, 685))
        self.window.blit(select_text, (235, 690))
        self.window.blit(UI.space_key, (360, 685))
        self.window.blit(use_text, (440, 690))

    def draw_skill_list(self, d_key_pressed, turn_order, current_turn, skill_selection_index=0):
        skill_selection_index %= len(turn_order[current_turn].skills)
        if d_key_pressed:
            font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 24)
            self.window.blit(UI.list_image, (15, 100))
            text = font.render("Skills", True, (255, 255, 255))
            self.window.blit(text, (140, 75))
            for i, skill in enumerate(turn_order[current_turn].skills):
                font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 16)
                rect = pygame.Rect(50, 125 + 67 * i, 255, 65)
                if i == skill_selection_index:
                    pygame.draw.rect(self.window, (255, 0, 0), rect, 2)

                skill_text = font.render(skill['name'] + ':', True, (255, 255, 255))
                self.window.blit(skill_text, (55, 130 + 67 * i))

                skill_text = font.render(str(skill['cost']), True, (255, 255, 0))
                self.window.blit(skill_text, (225, 130 + 67 * i))

                font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 12)
                for j, line in enumerate(skill['description'].split('\n')):
                    skill_text = font.render(line, True, (255, 255, 255))
                    self.window.blit(skill_text, (55, 150 + 67 * i + 12 * j))

    def draw_highlight(self, enter_key_pressed: bool, teams: dict, selection_index: int, is_attack: bool = True):
        player_team = teams['player_team']
        enemy_team = teams['enemy_team']
        player_team_highlight = teams['player_team_highlight']
        enemy_team_highlight = teams['enemy_team_highlight']
        if enter_key_pressed:
            if is_attack:
                self.window.blit(UI.enemy_highlight, (1000 - 24, 500 + 5 - 80 * enemy_team.index(
                    enemy_team_highlight[selection_index % len(enemy_team_highlight)])))
                self.window.blit(UI.enemy_frame_highlight, (1220 - 85 * enemy_team.index(
                    enemy_team_highlight[selection_index % len(enemy_team_highlight)]), 0))
            else:
                self.window.blit(UI.character_highlight, (600 - 24, 500 + 8 - 80 * player_team.index(
                    player_team_highlight[selection_index % len(player_team_highlight)])))
                self.window.blit(UI.character_frame_highlight, (
                    85 * player_team.index(player_team_highlight[selection_index % len(player_team_highlight)]) + 25,
                    0))

    def draw_turn_order(self, turn_order, current_turn_ui, player_team, enemy_team):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Plaguard.otf', 16)
        text_now = font.render("Now", True, (255, 255, 0))
        text_next = font.render("Next", True, (255, 255, 0))
        if turn_order[current_turn_ui % len(turn_order)].is_enemy():
            self.window.blit(text_now, (
                1223 - 85 * enemy_team.index(turn_order[current_turn_ui % len(turn_order)]), 2))
        else:
            self.window.blit(text_now, (
                28 + 85 * player_team.index(turn_order[current_turn_ui % len(turn_order)]), 2))

        if turn_order[(current_turn_ui + 1) % len(turn_order)].is_enemy():
            self.window.blit(text_next, (
                1223 - 85 * enemy_team.index(turn_order[(current_turn_ui + 1) % len(turn_order)]),
                2))
        else:
            self.window.blit(text_next, (
                28 + 85 * player_team.index(turn_order[(current_turn_ui + 1) % len(turn_order)]),
                2))
        pygame.display.update()

    def draw(self, player_team, enemy_team):
        self.window.fill((255, 255, 255))
        self.draw_background()
        self.draw_characters_list(player_team)
        self.draw_characters(player_team)
        self.draw_enemies(enemy_team)
        self.draw_enemy_list(enemy_team)
        self.draw_actions()