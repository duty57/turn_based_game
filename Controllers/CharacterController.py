import pygame
from turn_based_game.Controllers.Controller import Controller
from turn_based_game.Enums import CharacterState

pygame.mixer.init()

character_hit_sound = pygame.mixer.Sound('turn_based_game/audio/character_hit_sound.mp3')


class CharacterController(Controller):

    def __init__(self, actor, x: int = 200, y: int = 100):
        super().__init__(actor, x, y)
        # battle variables
        self.is_skill_selected = False
        self.in_inventory = False

        self.inventory_button_pressed = False
        self.unequipped_button_pressed = False
        self.left_arrow_pressed = False
        self.right_arrow_pressed = False
        self.up_arrow_pressed = False
        self.down_arrow_pressed = False
        self.enter_pressed = False

        self.character_index = 0
        self.selection_index = 0
        self.is_equipped = False
        self.is_unequipped = False

    def collide(self):
        if self.in_battle:
            character_hit_sound.play()
            self.character_state = CharacterState.hit

    def inventory_controller(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not self.left_arrow_pressed:
            self.character_index -= 1
            self.left_arrow_pressed = True
        elif not keys[pygame.K_LEFT]:
            self.left_arrow_pressed = False

        if keys[pygame.K_RIGHT] and not self.right_arrow_pressed:
            self.character_index += 1
            self.right_arrow_pressed = True
        elif not keys[pygame.K_RIGHT]:
            self.right_arrow_pressed = False

        if keys[pygame.K_UP] and not self.up_arrow_pressed:
            self.selection_index -= 1
            self.up_arrow_pressed = True
        elif not keys[pygame.K_UP]:
            self.up_arrow_pressed = False

        if keys[pygame.K_DOWN] and not self.down_arrow_pressed:
            self.selection_index += 1
            self.down_arrow_pressed = True
        elif not keys[pygame.K_DOWN]:
            self.down_arrow_pressed = False

        if keys[pygame.K_ESCAPE]:
            self.in_inventory = False

        if keys[pygame.K_RETURN]:
            if not self.enter_pressed:
                self.enter_pressed = True
                self.is_equipped = True
        else:
            self.enter_pressed = False
            self.is_equipped = False

        if keys[pygame.K_u]:
            if not self.is_unequipped:
                self.unequipped_button_pressed = True
                self.is_unequipped = True
        else:
            self.is_unequipped = False
            self.unequipped_button_pressed = False

    def perform_movement(self, move_x: int, move_y: int, collisions: list):
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
        self.world_x = self.x
        self.world_y = self.y
        self.actor.rect.center = (self.x, self.y)

    # Character controller
    def controller(self, window: pygame.Surface, adjusted_rect: pygame.Rect = None, collisions: list = None):

        keys = pygame.key.get_pressed()
        if collisions is None:
            collisions = []
        if self.character_state != CharacterState.inactive:
            if not self.in_battle:
                if keys[pygame.K_SPACE] and not self.character_state == CharacterState.hit:
                    self.character_state = CharacterState.attacking
                elif self.character_state != CharacterState.attacking and self.character_state != CharacterState.hit:
                    self.character_state = CharacterState.idle

                if keys[pygame.K_i]:
                    if not self.inventory_button_pressed:
                        self.in_inventory = not self.in_inventory
                        self.inventory_button_pressed = True
                else:
                    self.inventory_button_pressed = False

                if self.in_inventory:
                    self.inventory_controller()

                else:
                    move_x = 0
                    move_y = 0

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
                    self.perform_movement(move_x, move_y, collisions)
                return self.x, self.y

            else:
                if self.going_to_enemy:
                    self.go_to_enemy(self.target, 20)
                elif self.finished_attack:
                    self.go_back((self.battle_x, self.battle_y))

                # change character position
                self.actor.rect.center = (self.x, self.y)
        self.draw(window, adjusted_rect)

    def battle_start(self, i: int):
        self.x = 600
        self.y = 500 - 80 * i
        self.battle_x = 600
        self.battle_y = 500 - 80 * i
        self.actor.rect.center = (self.x, self.y)
        self.moving_right_direction = True
        self.moving_left_direction = False
        self.in_battle = True

    def attack_skill(self, skill: dict, enemy_team: list):  # may need to refactor this
        # check how many targets the skill can hit, then go to the target, hit target with skill and create vfx
        self.skill = skill
        self.actor.action_points -= skill['cost']
        self.going_to_enemy = True
        self.in_action = True
        self.enemy_team = enemy_team

    def healing_skill(self, skill: dict, player_team: list):  # may need to refactor this
        self.skill = skill
        self.actor.action_points -= skill['cost']
        self.in_action = True
        self.player_team = player_team
        self.character_state = CharacterState.healing

    def end_of_battle(self):
        self.x = self.world_x
        self.y = self.world_y
        self.in_battle = False
        self.finished_attack = False
        self.target = None
        self.enemy_team = None
        self.player_team = None
        self.character_state = CharacterState.idle
        self.actor.rect.center = (self.x, self.y)
        self.actor.health = 1 if self.actor.health == 0 else self.actor.health

    def adjust_rect(self, rect: pygame.Rect):
        return rect.move(-16, -10)
