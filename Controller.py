import pygame

from turn_based_game.Enums import CharacterState, CharacterBattleState


# TODO: remove draw/controllers from Actor, Character, and Enemy classes
# TODO: remove load_animations from Actor class
# TODO: remove states from Actor class

class Controller:

    def __init__(self, actor, animations: dict, x: int = 200, y: int = 100):
        self.actor = actor

        self.rect = None

        # world states
        self.moving_right_direction = True
        self.moving_left_direction = False
        self.finished_attack = False
        self.finished_hit = False

        # character state
        self.character_state = CharacterState.idle

        self.battle_x = 0
        self.battle_y = 0

        # battle states
        self.target = None
        self.going_to_enemy = False
        self.previous_battle_state = CharacterBattleState.init
        self.battle_state = CharacterBattleState.idle

        # Movement
        self.frameCount = 0
        self.attackFrameCount = 0
        self.hit_frame_count = 0
        self.deathFrameCount = 0
        self.x = x
        self.y = y

        self.profile = None
        self.health_bar = None
        self.action_points_bar = None

        self.health_bar_width = None
        self.action_points_bar_height = None

        self.in_battle = False
        self.in_action = False

        # Character animations
        self.idle = animations['idle']
        self.walkRight = animations['move_right']
        self.walkLeft = animations['move_right']
        self.attack = animations['attack']
        self.death = animations['dead']
        self.damageTaken = animations['hit']

    def draw(self, window, adjusted_rect=pygame.Rect(0, 0, 1280, 720)):

        walk_animation_length = len(self.walkRight)
        idle_animation_length = len(self.idle)
        attack_animation_length = len(self.attack)
        hit_animation_length = len(self.damageTaken)
        death_animation_length = len(self.death)

        if self.actor.__class__.__name__ == 'Enemy':
            if not self.in_battle:
                adjusted_rect = adjusted_rect.move(10, 10)
        else:
            adjusted_rect = adjusted_rect.move(-16, -10)

        if not self.in_battle and self.character_state != CharacterState.hit:
            self.finished_attack = False
            self.finished_hit = False  # maybe here is the problem with hit animations

        match self.character_state.value:
            case CharacterState.idle.value:
                frame_index = (self.frameCount // (
                        idle_animation_length * 4 // idle_animation_length)) % idle_animation_length
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.idle[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.idle[frame_index], adjusted_rect)
            case CharacterState.moving.value:
                if self.moving_right_direction:
                    frame_index = (self.frameCount // (
                            walk_animation_length * 4 // walk_animation_length)) % walk_animation_length
                    window.blit(self.walkRight[frame_index], adjusted_rect)
                elif self.moving_left_direction:
                    frame_index = (self.frameCount // (
                            walk_animation_length * 4 // walk_animation_length)) % walk_animation_length
                    window.blit(pygame.transform.flip(self.walkRight[frame_index], True, False), adjusted_rect)
            case CharacterState.attacking.value:
                frame_index = (self.attackFrameCount // (
                        attack_animation_length * 2 // attack_animation_length)) % attack_animation_length
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.attack[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.attack[frame_index], adjusted_rect)
                self.attackFrameCount += 1
                if self.attackFrameCount >= attack_animation_length * (30 // attack_animation_length):
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
                        hit_animation_length * 4 // hit_animation_length)) % hit_animation_length
                self.draw_damage(window)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.damageTaken[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.damageTaken[frame_index], adjusted_rect)
                self.hit_frame_count += 1
                if self.hit_frame_count >= hit_animation_length * (30 // death_animation_length):
                    self.character_state = CharacterState.idle
                    self.hit_frame_count = 0
                    self.finished_hit = True
            case CharacterState.dead.value:
                frame_index = (self.deathFrameCount // (
                        death_animation_length * 4 // death_animation_length)) % death_animation_length
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.death[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.death[frame_index], adjusted_rect)
                self.deathFrameCount += 1
                if self.deathFrameCount >= death_animation_length * (30 // death_animation_length):
                    self.character_state = CharacterState.inactive
                    self.deathFrameCount = 0

        self.frameCount += 1
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)
