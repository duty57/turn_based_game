
import pygame
from Enums import CharacterBattleState, CharacterState
from turn_based_game.Actor import Actor


class Character(Actor):

    def __init__(self, config_file: str, character_name: str, x: int = 200, y: int = 100):

        # Character States
        super().__init__(config_file, character_name, x, y)

    def level_up(self):
        self.level += 1

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.nextLevel:
            self.level_up()
            self.experience = 0
            self.nextLevel += 100 * self.level

    # Character controller
    def controller(self, keys, collisions=None):
        if collisions is None:
            collisions = []
        if self.character_state != CharacterState.inactive:
            move_x = 0
            move_y = 0
            if not self.in_battle:

                if keys[
                    pygame.K_SPACE] and self.character_class == 'Warrior' and not self.character_state == CharacterState.hit:
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
                    if obj.colliderect(self.rect.move(move_x * self.speed / 5, 0)):
                        move_x = 0
                    if obj.colliderect(self.rect.move(0, move_y * self.speed / 5)):
                        move_y = 0

                if move_x != 0 and move_y != 0:
                    move_x *= 0.7071  # 1/sqrt(2)
                    move_y *= 0.7071  # 1/sqrt(2)

                self.x += move_x * self.speed / 5
                self.y += move_y * self.speed / 5
                self.rect.center = (self.x, self.y)

            else:
                if self.going_to_enemy:
                    self.go_to_enemy(self.target)
                elif self.finished_attack:
                    self.go_back((self.battle_x, self.battle_y))

                # change character position
                self.rect.center = (self.x, self.y)

    # Draw the character
    def draw(self, window, adjusted_rect=pygame.Rect(0, 0, 1280, 720)):

        walkAnimationLength = len(self.walkRight)
        idleAnimationLength = len(self.idle)
        attackAnimationLength = len(self.attack)
        hitAnimationLength = len(self.damageTaken)
        deathAnimationLength = len(self.death)

        adjusted_rect = adjusted_rect.move(-16, -10)

        if not self.in_battle:
            self.finished_attack = False
            self.finished_hit = False  # maybe here is the problem with hit animations

        match self.character_state.value:
            case CharacterState.idle.value:
                frame_index = (self.frameCount // (
                        idleAnimationLength * 4 // idleAnimationLength)) % idleAnimationLength
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.idle[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.idle[frame_index], adjusted_rect)
            case CharacterState.moving.value:
                if self.moving_right_direction:
                    frame_index = (self.frameCount // (
                            walkAnimationLength * 4 // walkAnimationLength)) % walkAnimationLength
                    window.blit(self.walkRight[frame_index], adjusted_rect)
                elif self.moving_left_direction:
                    frame_index = (self.frameCount // (
                            walkAnimationLength * 4 // walkAnimationLength)) % walkAnimationLength
                    window.blit(pygame.transform.flip(self.walkRight[frame_index], True, False), adjusted_rect)
            case CharacterState.attacking.value:
                frame_index = (self.attackFrameCount // (
                        attackAnimationLength * 2 // attackAnimationLength)) % attackAnimationLength
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.attack[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.attack[frame_index], adjusted_rect)
                self.attackFrameCount += 1
                if self.attackFrameCount >= attackAnimationLength * (30 // deathAnimationLength):
                    self.attackFrameCount = 0
                    self.finished_attack = True
                    self.character_state = CharacterState.idle
                    if self.target:
                        self.previous_battle_state = self.battle_state
                        self.battle_state = CharacterBattleState.attacking
                        self.target.collide()
                        self.target.take_damage(30)
            case CharacterState.hit.value:
                frame_index = (self.hit_frame_count // (
                        hitAnimationLength * 4 // hitAnimationLength)) % hitAnimationLength
                self.draw_damage(window)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.damageTaken[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.damageTaken[frame_index], adjusted_rect)
                self.hit_frame_count += 1
                if self.hit_frame_count >= hitAnimationLength * (30 // deathAnimationLength):
                    self.character_state = CharacterState.idle
                    self.hit_frame_count = 0
                    self.finished_hit = True
            case CharacterState.dead.value:
                frame_index = (self.deathFrameCount // (
                        deathAnimationLength * 4 // deathAnimationLength)) % deathAnimationLength
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.death[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.death[frame_index], adjusted_rect)
                self.deathFrameCount += 1
                if self.deathFrameCount >= deathAnimationLength * (30 // deathAnimationLength):
                    self.character_state = CharacterState.inactive
                    self.deathFrameCount = 0

        self.frameCount += 1
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)

