import pygame

from turn_based_game.Actors.Character import Character
from turn_based_game.Controllers.Controller import Controller
from turn_based_game.Enums import CharacterState

pygame.mixer.init()
enemy_hit_sound = pygame.mixer.Sound('turn_based_game/audio/enemy_hit_sound.mp3')


def select_target(team: list):
    team.sort(key=lambda enemy: enemy.health)
    return team


class EnemyController(Controller):

    def __init__(self, actor, x: int = 200, y: int = 100, main_character=None):
        super().__init__(actor, x, y)
        self.patrol_points = [(x + 100, y), (x - 100, y), (x, y)]
        self.current_patrol_point = 0

        self.is_triggered = False
        self.main_character = main_character

        self.trigger_time = None
        self.in_battle = False

        self.is_skill_selected = False

    def collide(self):
        if self.in_battle:
            enemy_hit_sound.play()
            self.character_state = CharacterState.hit

    def set_main_character(self, main_character: Character):
        self.main_character = main_character

    def trigger(self):
        distance = abs(self.x - self.main_character.controller.x) ** 2 + abs(
            self.y - self.main_character.controller.y) ** 2
        looking_at_main_character = ((self.x < self.main_character.controller.x + 10) and self.moving_right_direction or
                                     (self.x > self.main_character.controller.x - 10) and self.moving_left_direction)
        if abs(self.x - self.main_character.controller.x) ** 2 + abs(
                self.y - self.main_character.controller.y) ** 2 < 25 ** 2:
            if self.trigger_time is None:
                self.trigger_time = pygame.time.get_ticks()  # Record the time when the enemy is triggered
            elif pygame.time.get_ticks() - self.trigger_time > 750:  # If 1 second has passed since the enemy was triggered
                self.character_state = CharacterState.attacking
                self.main_character.controller.collide()
                self.trigger_time = None
        elif distance < 100 ** 2 and looking_at_main_character:
            self.is_triggered = True
            self.patrol_points[-1] = (self.main_character.controller.x, self.main_character.controller.y - 25)
            self.current_patrol_point = 2
        elif self.is_triggered:
            self.is_triggered = False
            self.current_patrol_point = 0

    def controller(self, window: pygame.Surface, adjusted_rect: pygame.Rect = None):
        # patrol the area
        if self.character_state.value != CharacterState.inactive.value:
            if not self.in_battle:

                if self.character_state != CharacterState.attacking:
                    if self.x < self.patrol_points[self.current_patrol_point][0]:
                        self.moveRight()
                        self.move_to_target()

                    elif self.x > self.patrol_points[self.current_patrol_point][0]:
                        self.moveLeft()
                        self.move_to_target()
                    else:
                        self.current_patrol_point = (self.current_patrol_point + 1) % (len(self.patrol_points) - 1)
                self.actor.rect.center = (self.x, self.y)
                self.trigger()
            else:
                if self.going_to_enemy:
                    self.go_to_enemy(self.target, 40)
                elif self.finished_attack:
                    self.go_back((self.battle_x, self.battle_y))

                # change character position
                self.actor.rect.center = (self.x, self.y)

        self.draw(window, adjusted_rect)

    def move_to_target(self):
        if self.y + 5 < self.patrol_points[self.current_patrol_point][1]:
            self.moveDown()
        elif self.y - 25 > self.patrol_points[self.current_patrol_point][1]:
            self.moveUp()

    def battle_start(self, i: int):
        self.x = 1000
        self.y = 500 - 80 * i
        self.battle_x = 1000
        self.battle_y = 500 - 80 * i
        self.actor.rect.center = (self.x, self.y)
        self.moving_right_direction = False
        self.moving_left_direction = True
        self.in_battle = True

    def enemy_to_attack(self, enemy_team: list):
        enemies_with_weaknesses = []
        for skill in self.actor.skills:
            for enemy in enemy_team:
                if skill['element'] in enemy.weakness and skill['cost'] <= self.actor.action_points:
                    enemies_with_weaknesses.append(enemy)

            if enemies_with_weaknesses:
                self.skill = skill
                self.is_skill_selected = True
                return select_target(enemies_with_weaknesses)[0]

        for enemy in enemy_team:  # look for enemies with weaknesses to the actor's element
            if self.actor.element in enemy.weakness:
                enemies_with_weaknesses.append(enemy)

        if enemies_with_weaknesses:
            return select_target(enemies_with_weaknesses)[0]


        return enemy_team[enemy_team.index(min(enemy_team, key=lambda enemy: enemy.health))[0]]

    def attack_skill(self, enemy_team: list):  # may need to refactor this
        # check how many targets the skill can hit, then go to the target, hit target with skill and create vfx
        self.actor.action_points -= self.skill['cost']
        self.going_to_enemy = True
        self.in_action = True
        self.enemy_team = enemy_team

    def adjust_rect(self, rect: pygame.Rect):
        return rect.move(10, 10) if not self.in_battle else rect

    def __del__(self):
        print(f"Enemy controller has been defeated")
        del self.actor
