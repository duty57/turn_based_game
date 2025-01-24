import pygame
from turn_based_game.Controller import Controller
from turn_based_game.Enums import CharacterState


class CharacterController(Controller):

    def __init__(self, actor, x: int = 200, y: int = 100):
        super().__init__(actor, x, y)

    # Character controller
    def controller(self, window, adjusted_rect = None, collisions=None):
        keys = pygame.key.get_pressed()
        if collisions is None:
            collisions = []
        if self.character_state != CharacterState.inactive:
            move_x = 0
            move_y = 0
            if not self.in_battle:

                if keys[
                    pygame.K_SPACE] and not self.character_state == CharacterState.hit:
                    self.character_state = CharacterState.attacking
                elif self.character_state != CharacterState.attacking and self.character_state != CharacterState.hit:
                    self.character_state = CharacterState.idle

                if keys[pygame.K_LEFT]:
                    move_x = -1
                    self.moving_left_direction = True
                    self.moving_right_direction = False
                    self.character_state = CharacterState.moving
                elif keys[pygame.K_RIGHT]:
                    move_x = 1
                    self.moving_left_direction = False
                    self.moving_right_direction = True
                    self.character_state = CharacterState.moving

                if keys[pygame.K_UP]:
                    move_y = -1
                    self.character_state = CharacterState.moving
                elif keys[pygame.K_DOWN]:
                    move_y = 1
                    self.character_state = CharacterState.moving

                for obj in collisions:
                    if obj.colliderect(self.actor.rect.move(move_x * 2, 0)):
                        move_x = 0
                    if obj.colliderect(self.actor.rect.move(0, move_y * 2)):
                        move_y = 0

                if move_x != 0 and move_y != 0:
                    move_x *= 0.7071  # 1/sqrt(2)
                    move_y *= 0.7071  # 1/sqrt(2)

                self.x += move_x * 2
                self.y += move_y * 2
                self.actor.rect.center = (self.x, self.y)
                return self.x, self.y

            else:
                if self.going_to_enemy:
                    self.go_to_enemy(self.target)
                elif self.finished_attack:
                    self.go_back((self.battle_x, self.battle_y))

                # change character position
                self.actor.rect.center = (self.x, self.y)
        self.draw(window, adjusted_rect)
