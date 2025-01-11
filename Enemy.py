from math import sqrt
from time import sleep

import pygame

from turn_based_game.Character import Character
from turn_based_game.Enums import CharacterBattleState, CharacterState


class Enemy(Character):
    def __init__(self, config, characterName, x, y, main_character=None):
        super().__init__(config, characterName, x, y)
        self.enemy = True

        self.patrol_points = [(x+100, y), (x-100, y), (x, y)]
        self.current_patrol_point = 0

        self.is_triggered = False
        self.main_character = main_character

        self.trigger_time = None
        self.in_battle = False



    def set_main_character(self, main_character):
        self.main_character = main_character

    def moveRight(self):
        self.x += 1 if not self.in_battle else 2
        self.moving_right_direction = True
        self.moving_left_direction = False
        self.character_state = CharacterState.moving

    def moveLeft(self):
        self.x -= 1 if not self.in_battle else 2
        self.moving_right_direction = False
        self.moving_left_direction = True
        self.character_state = CharacterState.moving
    def moveUp(self):
        self.y -= 1 if not self.in_battle else 2
        self.character_state = CharacterState.moving
    def moveDown(self):
        self.y += 1 if not self.in_battle else 2
        self.character_state = CharacterState.moving
    def trigger(self):
        distance = abs(self.x - self.main_character.x)**2 + abs(self.y - self.main_character.y)**2
        looking_at_main_character = (self.x < self.main_character.x + 10) and self.moving_right_direction or (self.x > self.main_character.x - 10) and self.moving_left_direction
        if abs(self.x - self.main_character.x)**2 + abs(self.y - self.main_character.y)**2 < 25**2:
            if self.trigger_time is None:
                self.trigger_time = pygame.time.get_ticks()  # Record the time when the enemy is triggered
            elif pygame.time.get_ticks() - self.trigger_time > 500:  # If 1 second has passed since the enemy was triggered
                self.character_state = CharacterState.attacking
                self.main_character.collide()
                self.trigger_time = None
        elif distance < 100**2 and looking_at_main_character:
            self.is_triggered = True
            self.patrol_points[-1] = (self.main_character.x, self.main_character.y)
            self.current_patrol_point = 2
        elif self.is_triggered:
            self.is_triggered = False
            self.current_patrol_point = 0

    def controller(self):
        # patrol the area
        if not self.in_battle:

            if self.character_state != CharacterState.attacking:
                if self.x < self.patrol_points[self.current_patrol_point][0]:
                    self.moveRight()
                    if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
                        self.moveDown()
                    elif self.y - 10 > self.patrol_points[self.current_patrol_point][1]:
                        self.moveUp()


                elif self.x > self.patrol_points[self.current_patrol_point][0]:
                    self.moveLeft()
                    if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
                        self.moveDown()
                    elif self.y - 10 > self.patrol_points[self.current_patrol_point][1]:
                        self.moveUp()
                else:
                    self.current_patrol_point = (self.current_patrol_point + 1) % (len(self.patrol_points) - 1)
            self.rect.topleft = (self.x, self.y)
            self.trigger()
        else:
            if self.going_to_enemy:
                self.go_to_enemy(self.target)
            elif self.finished_attack:
                self.go_back((self.battle_x, self.battle_y))

            # change character position
            self.rect.center = (self.x, self.y)


    def draw(self, window, adjusted_rect=pygame.Rect(0, 0, 1280, 720)):
        walkAnimationLength = len(self.walkRight)
        idleAnimationLength = len(self.idle)
        attackAnimationLength = len(self.attack)
        hitAnimationLength = len(self.damageTaken)

        if self.character_state.value == CharacterState.hit.value:
            frame_index = (self.frameCount // (hitAnimationLength * 4 // hitAnimationLength)) % hitAnimationLength
            if self.moving_left_direction:
                window.blit(pygame.transform.flip(self.damageTaken[frame_index], True, False), adjusted_rect)
            else:
                window.blit(self.damageTaken[frame_index], adjusted_rect)
            self.frameCount += 1
            if self.frameCount >= hitAnimationLength * 3:
                self.character_state = CharacterState.idle
                self.frameCount = 0
                self.finished_hit = True

        if not self.enemy:
            adjusted_rect = adjusted_rect.move(-16, -10)

        if not self.in_battle and self.character_state != CharacterState.hit:
            self.finished_attack = False
            self.finished_hit = False


        match self.character_state:
            case CharacterState.idle:
                frame_index = (self.frameCount // (
                            idleAnimationLength * 4 // idleAnimationLength)) % idleAnimationLength
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.idle[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.idle[frame_index], adjusted_rect)
            case CharacterState.moving:
                if self.moving_right_direction:
                    frame_index = (self.frameCount // (
                                walkAnimationLength * 4 // walkAnimationLength)) % walkAnimationLength
                    window.blit(self.walkRight[frame_index], adjusted_rect)
                elif self.moving_left_direction:
                    frame_index = (self.frameCount // (
                                walkAnimationLength * 4 // walkAnimationLength)) % walkAnimationLength
                    window.blit(pygame.transform.flip(self.walkRight[frame_index], True, False), adjusted_rect)
            case CharacterState.attacking:
                frame_index = (self.attackFrameCount // (
                            attackAnimationLength * 2 // attackAnimationLength)) % attackAnimationLength
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.attack[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.attack[frame_index], adjusted_rect)
                self.attackFrameCount += 1
                if self.attackFrameCount >= attackAnimationLength * 2:
                    self.attackFrameCount = 0
                    self.finished_attack = True
                    self.character_state = CharacterState.idle
                    if self.target:
                        self.target.collide()
                        self.target.take_damage(5)

        self.frameCount += 1
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)

    def go_to_enemy(self, enemy):
        if self.x < enemy.rect.x - 40:
            self.moveRight()
        elif self.x > enemy.rect.x + 40:
            self.moveLeft()
        if self.y < enemy.rect.center[1]:
            self.moveDown()
        elif self.y > enemy.rect.center[1]:
            self.moveUp()

        if self.rect.center == (self.x, self.y):
            self.going_to_enemy = False
            self.character_state = CharacterState.attacking

    def go_back(self, position):
        if self.x < position[0]:
            self.moveRight()
        if self.y < position[1]:
            self.moveDown()
        if self.x > position[0]:
            self.moveLeft()
        if self.y > position[1]:
            self.moveUp()

        if self.rect.center == (self.x, self.y):
            self.in_action = False
            self.character_state = CharacterState.idle
            self.finished_attack = False
            self.moving_right_direction = False
            self.moving_left_direction = True
            # self.battle_state = CharacterBattleState.back_in_position

#TODO: Attack animation when is closer than 25 pixels
#TODO: Register collision with main character
           #
           # else:
           #      self.moving_right_direction = False
           #      self.moving_left_direction = True
           #      self.character_state = CharacterState.idle