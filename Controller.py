import random

import pygame

from turn_based_game.Enums import CharacterState, CharacterBattleState
from turn_based_game.VFX import VFX


def get_frame_index(frame_count, k, vfx_animation):
    return (frame_count // (len(vfx_animation) * k // len(vfx_animation))) % len(vfx_animation)


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
        self.skill = None
        self.enemy_team = None
        self.player_team = None

        # Movement
        self.frameCount = 0
        self.attack_frame_count = 0
        self.hit_frame_count = 0
        self.death_frame_count = 0
        self.vfx_frame_count = 0
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
        self.attack = None
        self.death = None
        self.damage_taken = None

        self.is_weak = False

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
        self.attack = animations['attack']
        self.death = animations['dead']
        self.damage_taken = animations['hit']

    def heal(self, heal_amount):
        self.actor.health += heal_amount
        if self.actor.health > self.actor.max_health:
            self.actor.health = self.actor.max_health

    def take_damage(self, damage, element):
        self.collide()
        chance = random.randint(1, 100)
        if chance <= self.actor.agility:
            self.actor.damage = -1
            return

        if self.character_state.value != CharacterState.inactive.value:
            if element in self.actor.immunity:
                self.actor.damage = 0
                self.actor.is_weak = False
            elif element in self.actor.weakness:
                self.actor.damage = int(damage * 2)
                self.actor.is_weak = True
            else:
                self.actor.damage = int(damage)
                self.actor.is_weak = False

            self.actor.health -= self.actor.damage
            if self.actor.health <= 0:
                self.actor.health = 0
                self.character_state = CharacterState.dead

    def collide(self):
        if self.in_battle:
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

    def perform_attack(self):
        if self.skill:
            if self.skill['targets'] == 'all':
                for enemy in self.enemy_team:
                    enemy.controller.take_damage(self.skill['value'], self.skill['element'])
            else:
                self.target.controller.take_damage(self.skill['value'], self.skill['element'])
        else:
            self.target.controller.take_damage(self.actor.damage, self.actor.element)

        self.skill = None

    def draw_vfx(self, window):
        if not self.in_action:
            return

        if self.skill:
            element = self.skill['element']
            vfx_animation = VFX.skills.get(element, [])
            if self.skill['targets'] == 'all':
                frame_index = get_frame_index(self.vfx_frame_count, 4, vfx_animation)
                vfx_image = pygame.image.load(vfx_animation[frame_index])
                for enemy in self.enemy_team:
                    target_position = (enemy.rect.center[0] - 15, enemy.rect.center[1] - 20)
                    window.blit(vfx_image, target_position)
                self.vfx_frame_count += 1
                if self.vfx_frame_count >= len(vfx_animation) * (30 // len(vfx_animation)):
                    self.vfx_frame_count = 0
            else:
                self._draw_vfx_for_single_target(window, vfx_animation)
        else:
            vfx_animation = VFX.skills.get(self.actor.element, [])
            self._draw_vfx_for_single_target(window, vfx_animation)

    def _draw_vfx_for_single_target(self, window, vfx_animation):
        if not vfx_animation:
            return
        frame_index = get_frame_index(self.vfx_frame_count, 4, vfx_animation)
        vfx_image = pygame.image.load(vfx_animation[frame_index])
        target_position = (self.target.rect.center[0] - 15, self.target.rect.center[1] - 20)
        window.blit(vfx_image, target_position)
        self.vfx_frame_count += 1
        if self.vfx_frame_count >= len(vfx_animation) * (30 // len(vfx_animation)):
            self.vfx_frame_count = 0
            self.skill = None

    def draw(self, window, adjusted_rect=pygame.Rect(0, 0, 1280, 720)):

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
                frame_index = get_frame_index(self.frameCount, 4, self.idle)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.idle[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.idle[frame_index], adjusted_rect)
            case CharacterState.moving.value:
                frame_index = get_frame_index(self.frameCount, 4, self.walkRight)
                if self.moving_right_direction:
                    window.blit(self.walkRight[frame_index], adjusted_rect)
                elif self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.walkRight[frame_index], True, False), adjusted_rect)
            case CharacterState.attacking.value:
                self.draw_vfx(window)
                frame_index = get_frame_index(self.attack_frame_count, 2, self.attack)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.attack[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.attack[frame_index], adjusted_rect)
                self.attack_frame_count += 1
                if self.attack_frame_count >= len(self.attack) * (30 // len(self.attack)):
                    self.attack_frame_count = 0
                    self.finished_attack = True
                    self.character_state = CharacterState.idle
                    if self.target:
                        self.previous_battle_state = self.battle_state
                        self.battle_state = CharacterBattleState.attacking
                        self.perform_attack()
            case CharacterState.hit.value:
                frame_index = get_frame_index(self.hit_frame_count, 4, self.damage_taken)
                self.draw_damage(window)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.damage_taken[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.damage_taken[frame_index], adjusted_rect)
                self.hit_frame_count += 1
                if self.hit_frame_count >= len(self.damage_taken) * (30 // len(self.damage_taken)):
                    self.character_state = CharacterState.idle
                    self.hit_frame_count = 0
                    self.finished_hit = True
            case CharacterState.dead.value:
                frame_index = get_frame_index(self.death_frame_count, 4, self.death)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.death[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.death[frame_index], adjusted_rect)
                self.death_frame_count += 1
                if self.death_frame_count >= len(self.death) * (
                        29 // len(self.death)):  # TODO goblin death animation is not working when 30 is used
                    self.character_state = CharacterState.inactive
                    self.death_frame_count = 0

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
        window.blit(health_text, (offset - 15, 48))

        # Action points value
        action_points_text = font.render(str(self.actor.action_points), True, (255, 200, 37))
        window.blit(action_points_text, (offset - 22, 35))

        if self.character_state.value >= CharacterState.dead.value:
            window.blit(death_frame, (offset, 0))

    def draw_damage(self, window):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 16)
        if self.actor.damage > 0:
            damage_text = f"WEAK: {self.actor.damage}" if self.actor.is_weak else str(self.actor.damage)
            self.is_weak = False
            damage_text = font.render(damage_text, True, (255, 0, 0))
        elif self.actor.damage < 0:
            damage_text = font.render("Miss", True, (255, 255, 255))
        else:
            damage_text = font.render("Immune", True, (178, 178, 172))

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

        if self.actor.rect.center == (self.x, self.y):  # check if the character is in the enemy position
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
            self.moving_right_direction = not self.actor.is_enemy()
            self.moving_left_direction = self.actor.is_enemy()
            self.previous_battle_state = self.battle_state
            self.battle_state = CharacterBattleState.back_in_position
