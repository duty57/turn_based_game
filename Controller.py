import random
import pygame
from turn_based_game.Enums import CharacterState, CharacterBattleState
from turn_based_game.VFX import VFX
from turn_based_game.ActorRenderer import ActorRenderer


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
        self.world_x = 0
        self.world_y = 0
        # battle states
        self.target = None
        self.going_to_enemy = False
        self.previous_battle_state = CharacterBattleState.init
        self.battle_state = CharacterBattleState.idle
        self.skill = None
        self.enemy_team = None
        self.player_team = None
        # Movement
        self.x = x
        self.y = y
        self.in_battle = False
        self.in_action = False
        self.is_weak = False
        self.actor_renderer = ActorRenderer()

    def load_animations(self, animations: dict):#load animations for the character
        self.actor_renderer.load_animations(animations)

    def heal(self, heal_amount):
        self.actor.health = min(self.actor.health + heal_amount, self.actor.max_health)

    def take_damage(self, damage, element, skill=None):
        self.collide()
        chance = random.randint(1, 100)
        instant_kill_chance = 100 - skill.get('instant_kill_chance', 0) if skill and skill.get('instant_kill_chance',
                                                                                               0) != 0 else 0
        if chance <= self.actor.agility + instant_kill_chance or chance <= self.actor.agility:
            self.actor.damage = -1
            return

        if self.character_state.value != CharacterState.inactive.value:
            if element in self.actor.immunity:
                self.actor.damage = 0
                self.is_weak = False
            elif element in self.actor.weakness:
                self.actor.damage = int(damage * 2)
                self.is_weak = True
            else:
                self.actor.damage = max(0, damage - self.actor.defense)
                self.is_weak = False

            self.actor.health -= self.actor.damage
            if self.actor.health <= 0:
                self.actor.health = 0
                self.character_state = CharacterState.dead

    def collide(self):
        pass

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

    def check_direction(self, window, frame_index, animation, adjusted_rect):
        if self.moving_left_direction:
            window.blit(pygame.transform.flip(animation[frame_index], True, False), adjusted_rect)
        else:
            window.blit(animation[frame_index], adjusted_rect)

    def perform_attack(self):
        if self.skill:
            if self.skill['targets'] == 'all':
                for enemy in self.enemy_team:
                    enemy.controller.take_damage(self.skill['value'], self.skill['element'], self.skill)
            else:
                self.target.controller.take_damage(self.skill['value'], self.skill['element'], self.skill)
        else:
            self.target.controller.take_damage(self.actor.strength, self.actor.element, self.skill)

        self.skill = None

    def adjust_rect(self, rect):
        pass

    def draw(self, window, adjusted_rect=pygame.Rect(0, 0, 1280, 720)):
        adjusted_rect = self.adjust_rect(adjusted_rect)

        if not self.in_battle and self.character_state != CharacterState.hit:
            self.finished_attack = False
            self.finished_hit = False  # maybe here is the problem with hit animations

        match self.character_state.value:
            case CharacterState.idle.value:
                self.actor_renderer.manage_idle_animation(window, adjusted_rect, self.moving_left_direction)
            case CharacterState.moving.value:
                self.actor_renderer.manage_move_animation(window, adjusted_rect, self.moving_left_direction)
            case CharacterState.attacking.value:
                self.manage_attack_animation(window, adjusted_rect)
            case CharacterState.hit.value:
                self.manage_hit_animation(adjusted_rect, window)
            case CharacterState.dead.value:
                self.manage_death_animation(adjusted_rect, window)
            case CharacterState.healing.value:
                self.manage_healing_animation(adjusted_rect, window)

        pygame.draw.rect(window, (255, 0, 0), self.actor.rect, 2)

    def manage_attack_animation(self, window, adjusted_rect):
        if self.in_action:
            self.actor_renderer.attack_vfx(window, self.skill, self.enemy_team, self.target, self.actor)
        self.actor_renderer.manage_attack_animation(window, adjusted_rect, self.moving_left_direction)
        if self.actor_renderer.attack_frame_count >= len(self.actor_renderer.attack) * (
                30 // len(self.actor_renderer.attack)):
            self.actor_renderer.attack_frame_count = 0
            self.finished_attack = True
            self.character_state = CharacterState.idle
            if self.target:
                self.previous_battle_state = self.battle_state
                self.battle_state = CharacterBattleState.attacking
                self.perform_attack()

    def manage_hit_animation(self, adjusted_rect, window):
        self.actor_renderer.draw_damage(window, self.actor, self.is_weak)
        self.actor_renderer.manage_hit_animation(window, adjusted_rect, self.moving_left_direction)
        if self.actor_renderer.hit_frame_count >= len(self.actor_renderer.damage_taken) * (
                30 // len(self.actor_renderer.damage_taken)):
            self.character_state = CharacterState.idle
            self.actor_renderer.hit_frame_count = 0
            self.finished_hit = True

    def manage_death_animation(self, adjusted_rect, window):
        self.actor_renderer.manage_death_animation(window, adjusted_rect, self.moving_left_direction)
        if self.actor_renderer.death_frame_count >= len(self.actor_renderer.death) * (
                29 // len(self.actor_renderer.death)):
            self.character_state = CharacterState.inactive
            self.actor_renderer.death_frame_count = 0

    def manage_healing_animation(self, adjusted_rect, window):
        self.actor_renderer.manage_heal_animation(window, adjusted_rect, self.moving_left_direction)
        self.actor_renderer.draw_heal(window, self.target, self.skill['value'])
        self.actor_renderer.heal_vfx(window, self.target)
        element = 'MAGIC'
        vfx_animation = VFX.skills.get(element, [])
        if self.actor_renderer.vfx_frame_count >= len(vfx_animation) * (30 // len(vfx_animation)):
            self.actor_renderer.vfx_frame_count = 0
            self.target.controller.heal(self.skill['value'])
            self.in_action = False
            self.previous_battle_state = CharacterBattleState.attacking
            self.battle_state = CharacterBattleState.back_in_position
            self.character_state = CharacterState.idle
            self.skill = None

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

    def go_to_enemy(self, enemy, offset):
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
