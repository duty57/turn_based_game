import pygame

from turn_based_game.Controller import Controller
from turn_based_game.Enums import CharacterState


class EnemyController(Controller):

    def __init__(self, actor, update_rect_callback, x: int = 200, y: int = 100, main_character=None):
        super().__init__(actor, update_rect_callback, x, y)
        self.patrol_points = [(x + 100, y), (x - 100, y), (x, y)]
        self.current_patrol_point = 0

        self.is_triggered = False
        self.main_character = main_character

        self.trigger_time = None
        self.in_battle = False

    def set_main_character(self, main_character):
        self.main_character = main_character

    def trigger(self):
        distance = abs(self.x - self.main_character.x) ** 2 + abs(self.y - self.main_character.y) ** 2
        looking_at_main_character = (self.x < self.main_character.x + 10) and self.moving_right_direction or (
                self.x > self.main_character.x - 10) and self.moving_left_direction
        if abs(self.x - self.main_character.x) ** 2 + abs(self.y - self.main_character.y) ** 2 < 25 ** 2:
            if self.trigger_time is None:
                self.trigger_time = pygame.time.get_ticks()  # Record the time when the enemy is triggered
            elif pygame.time.get_ticks() - self.trigger_time > 1500:  # If 1 second has passed since the enemy was triggered
                self.character_state = CharacterState.attacking
                self.main_character.collide()
                self.trigger_time = None
        elif distance < 100 ** 2 and looking_at_main_character:
            self.is_triggered = True
            self.patrol_points[-1] = (self.main_character.x, self.main_character.y - 25)
            self.current_patrol_point = 2
        elif self.is_triggered:
            self.is_triggered = False
            self.current_patrol_point = 0

    def controller(self, window, rect, adjusted_rect=None):
        # patrol the area
        if self.character_state.value != CharacterState.inactive.value:
            if not self.in_battle:

                if self.character_state != CharacterState.attacking:
                    if self.x < self.patrol_points[self.current_patrol_point][0]:
                        self.moveRight()
                        if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
                            self.moveDown()
                        elif self.y - 5 > self.patrol_points[self.current_patrol_point][1]:
                            self.moveUp()


                    elif self.x > self.patrol_points[self.current_patrol_point][0]:
                        self.moveLeft()
                        if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
                            self.moveDown()
                        elif self.y - 5 > self.patrol_points[self.current_patrol_point][1]:
                            self.moveUp()
                    else:
                        self.current_patrol_point = (self.current_patrol_point + 1) % (len(self.patrol_points) - 1)
                rect.center = (self.x, self.y)
                self.update_rect(self.x, self.y)
                self.trigger()
            else:
                if self.going_to_enemy:
                    self.go_to_enemy(self.target, rect)
                elif self.finished_attack:
                    self.go_back((self.battle_x, self.battle_y), rect)

                # change character position
                rect.center = (self.x, self.y)
                self.update_rect(self.x, self.y)

        self.draw(window, rect, adjusted_rect)
