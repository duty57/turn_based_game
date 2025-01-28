import pygame

from turn_based_game.Dataclasses.VFX import VFX


def get_frame_index(frame_count, k, vfx_animation):
    return (frame_count // (len(vfx_animation) * k // len(vfx_animation))) % len(vfx_animation)


class ActorRenderer:

    def __init__(self):
        self.frame_count = 0
        self.attack_frame_count = 0
        self.hit_frame_count = 0
        self.death_frame_count = 0
        self.vfx_frame_count = 0

        # Character animations
        self.idle = None
        self.walkRight = None
        self.attack = None
        self.death = None
        self.damage_taken = None

    def load_animations(self, animations: dict):
        self.idle = animations['idle']
        self.walkRight = animations['move_right']
        self.attack = animations['attack']
        self.death = animations['dead']
        self.damage_taken = animations['hit']

    def check_direction(self, moving_left_direction, window, frame_index, animation, adjusted_rect):
        if moving_left_direction:
            window.blit(pygame.transform.flip(animation[frame_index], True, False), adjusted_rect)
        else:
            window.blit(animation[frame_index], adjusted_rect)

    def draw_heal(self, window, target, heal_value=0):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 16)
        heal_text = font.render(str(heal_value), True, (0, 255, 0))
        window.blit(heal_text, (target.controller.x, target.controller.y - 50))

    def draw_damage(self, window, actor, is_weak):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 16)
        if actor.damage > 0:
            damage_text = f"WEAK: {actor.damage}" if is_weak else str(actor.damage)
            damage_text = font.render(damage_text, True, (255, 0, 0))
        elif actor.damage == -100:
            damage_text = font.render("Miss", True, (255, 255, 255))
        elif actor.damage == -1:
            damage_text = font.render("Immune", True, (178, 178, 172))
        else:
            damage_text = font.render("Blocked", True, (178, 178, 172))

        window.blit(damage_text, (actor.controller.x, actor.controller.y - 50))

    def heal_vfx(self, window, target):
        element = 'MAGIC'
        vfx_animation = VFX.skills.get(element, [])
        frame_index = get_frame_index(self.vfx_frame_count, 4, vfx_animation)
        vfx_image = pygame.image.load(vfx_animation[frame_index])
        target_position = (target.rect.center[0] - 15, target.rect.center[1] - 20)
        window.blit(vfx_image, target_position)
        self.vfx_frame_count += 1

    def attack_vfx(self, window, skill, enemy_team, target, actor):

        if skill:
            element = skill['element']
            vfx_animation = VFX.skills.get(element, [])
            if skill['targets'] == 'all':
                frame_index = get_frame_index(self.vfx_frame_count, 4, vfx_animation)
                vfx_image = pygame.image.load(vfx_animation[frame_index])
                for enemy in enemy_team:
                    target_position = (enemy.rect.center[0] - 15, enemy.rect.center[1] - 20)
                    window.blit(vfx_image, target_position)
                self.vfx_frame_count += 1
                if self.vfx_frame_count >= len(vfx_animation) * (30 // len(vfx_animation)):
                    self.vfx_frame_count = 0
            else:
                self._draw_vfx_for_single_target(window, vfx_animation, target)
        else:
            vfx_animation = VFX.skills.get(actor.element, [])
            self._draw_vfx_for_single_target(window, vfx_animation, target)

    def _draw_vfx_for_single_target(self, window, vfx_animation, target):
        if not vfx_animation:
            return
        frame_index = get_frame_index(self.vfx_frame_count, 4, vfx_animation)
        vfx_image = pygame.image.load(vfx_animation[frame_index])
        target_position = (target.rect.center[0] - 15, target.rect.center[1] - 20)
        window.blit(vfx_image, target_position)
        self.vfx_frame_count += 1
        if self.vfx_frame_count >= len(vfx_animation) * (30 // len(vfx_animation)):
            self.vfx_frame_count = 0

    def manage_idle_animation(self, window, adjusted_rect, moving_left_direction):
        frame_index = get_frame_index(self.frame_count, 4, self.idle)
        self.check_direction(moving_left_direction, window, frame_index, self.idle, adjusted_rect)
        self.frame_count += 1

    def manage_move_animation(self, window, adjusted_rect, moving_left_direction):
        frame_index = get_frame_index(self.frame_count, 4, self.walkRight)
        self.check_direction(moving_left_direction, window, frame_index, self.walkRight, adjusted_rect)
        self.frame_count += 1

    def manage_attack_animation(self, window, adjusted_rect, moving_left_direction):
        frame_index = get_frame_index(self.attack_frame_count, 2, self.attack)
        self.check_direction(moving_left_direction, window, frame_index, self.attack, adjusted_rect)
        self.attack_frame_count += 1

    def manage_hit_animation(self, window, adjusted_rect, moving_left_direction):
        frame_index = get_frame_index(self.hit_frame_count, 2, self.damage_taken)
        self.check_direction(moving_left_direction, window, frame_index, self.damage_taken, adjusted_rect)
        self.hit_frame_count += 1

    def manage_death_animation(self, window, adjusted_rect, moving_left_direction):
        frame_index = get_frame_index(self.death_frame_count, 4, self.death)
        self.check_direction(moving_left_direction, window, frame_index, self.death, adjusted_rect)
        self.death_frame_count += 1

    def manage_heal_animation(self, window, adjusted_rect, moving_left_direction):
        frame_index = get_frame_index(self.frame_count, 4, self.idle)
        self.check_direction(moving_left_direction, window, frame_index, self.idle, adjusted_rect)
        self.frame_count += 1