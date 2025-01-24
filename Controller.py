import pygame

from turn_based_game.Enums import CharacterState, CharacterBattleState


# TODO: remove draw/controllers from Actor, Character, and Enemy classes
# TODO: remove load_animations from Actor class
# TODO: remove states from Actor class

class Controller:

    def __init__(self, actor, x: int = 200, y: int = 100):
        self.actor = actor

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
        self.idle = None
        self.walkRight = None
        self.walkLeft = None
        self.attack = None
        self.death = None
        self.damageTaken = None

    # Load UI for the character
    def load_ui(self, profile: pygame.Surface, health_bar: pygame.Surface, action_points: pygame.Surface):
        self.profile = profile
        self.health_bar = health_bar
        self.action_points_bar = action_points
        self.health_bar_width = self.health_bar.get_width()
        self.action_points_bar_height = self.action_points_bar.get_height()

    def load_animations(self, animations: dict):
        self.idle = animations['idle']
        self.walkRight = animations['move_right']
        self.walkLeft = animations['move_right']
        self.attack = animations['attack']
        self.death = animations['dead']
        self.damageTaken = animations['hit']

    def take_damage(self, damage):
        if self.character_state.value != CharacterState.inactive.value:
            self.actor.damage = damage
            self.actor.health -= damage
            if self.actor.health <= 0:
                self.actor.health = 0
                self.character_state = CharacterState.dead

    def collide(self):
        self.character_state = CharacterState.hit

    def moveRight(self):
        self.x += 1 if not self.in_battle else 5
        self.moving_right_direction = True
        self.moving_left_direction = False
        self.character_state = CharacterState.moving

    def moveLeft(self):
        self.x -= 1 if not self.in_battle else 5
        self.moving_right_direction = False
        self.moving_left_direction = True
        self.character_state = CharacterState.moving

    def moveUp(self):
        self.y -= 1 if not self.in_battle else 5
        self.character_state = CharacterState.moving

    def moveDown(self):
        self.y += 1 if not self.in_battle else 5
        self.character_state = CharacterState.moving

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
                        self.target.controller.collide()
                        self.target.controller.take_damage(30)
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
        pygame.draw.rect(window, (255, 0, 0), self.actor.rect, 2)

    def draw_ui(self, window, profile_frame, death_frame, health_bar_frame, action_points_frame, offset):

        # calculate the health and action points percentage
        health_percentage = self.actor.health / self.actor.max_health
        action_points_percentage = self.actor.action_points / self.actor.max_action_points

        self.health_bar = pygame.transform.scale(self.health_bar, (
            int(self.health_bar_width * health_percentage), self.health_bar.get_height()))
        self.action_points_bar = pygame.transform.scale(self.action_points_bar, (
            self.action_points_bar.get_width(), int(self.action_points_bar_height * action_points_percentage)))

        adjust_action_points_bar = 0

        # adjust the action points bar
        if (self.action_points_bar_height - self.action_points_bar.get_height()) > 0:
            adjust_action_points_bar = (self.action_points_bar_height - self.action_points_bar.get_height()) - 1

        window.blit(profile_frame, (offset, 0))  # profile frame
        window.blit(self.profile, (offset + 5, 0 + 5))  # profile
        window.blit(self.health_bar, (offset + 13, 50 + 3))  # health bar
        window.blit(health_bar_frame, (offset + 10, 50))  # health bar frame
        window.blit(action_points_frame, (offset - 12, 5))  # action points frame
        window.blit(self.action_points_bar, (offset - 9, 5 + adjust_action_points_bar))  # action points bar

        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 12)

        # Health value
        health_text = font.render(str(self.actor.health), True, (217, 15, 30))
        # health_text = pygame.transform.rotate(health_text, 45)
        window.blit(health_text, (offset - 15, 48))

        # Action points value
        action_points_text = font.render(str(self.actor.action_points), True, (255, 200, 37))
        window.blit(action_points_text, (offset - 22, 35))

        if self.character_state.value >= CharacterState.dead.value:
            window.blit(death_frame, (offset, 0))

    def draw_damage(self, window):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 16)
        damage_text = font.render('-' + str(self.actor.damage), True, (255, 0, 0))
        window.blit(damage_text, (self.x, self.y - 50))

    def go_to_enemy(self, enemy):

        offset = 20

        if self.__class__.__name__ == "Enemy":
            offset = 40

        if self.x < enemy.rect.x - offset:
            self.moveRight()
        elif self.x > enemy.rect.x + offset:
            self.moveLeft()
        if self.y < enemy.rect.center[1]:
            self.moveDown()
        elif self.y > enemy.rect.center[1]:
            self.moveUp()

        if self.actor.rect.center == (self.x, self.y):
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

        if self.actor.rect.center == (self.x, self.y):
            self.in_action = False
            self.character_state = CharacterState.idle
            self.finished_attack = False
            self.moving_right_direction = self.__class__.__name__ != "Enemy"
            self.moving_left_direction = self.__class__.__name__ == "Enemy"
            self.previous_battle_state = self.battle_state
            self.battle_state = CharacterBattleState.back_in_position
