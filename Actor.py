import json

import pygame
from Enums import CharacterBattleState, CharacterState


# TODO formula for enemy leveling: player_level + 1 * (player_level // 5)
class Actor(pygame.sprite.Sprite):
    def __init__(self, config_file: str, character_name: str, x: int = 200, y: int = 100):

        # Character States
        super().__init__()
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
        self.idle = None
        self.walkRight = None
        self.walkLeft = None
        self.attack = None
        self.death = None
        self.damageTaken = None

        # Read JSON file with character information
        with open(config_file) as file:
            data = json.load(file)
            data = data[character_name]
            self.name = data['name']

            # Character attributes
            self.immunity = data['immunity']
            self.weakness = data['weakness']
            self.element = data['element']
            self.skills = data.get('skills', [])

            self.max_health = data['maxHealth']
            self.strength = data['strength']
            self.intelligence = data['intelligence']
            self.defense = data['defense']
            self.speed = data['speed']
            self.agility = data['agility']
            self.max_action_points = data['actionPoints']

            self.character_class = data['characterClass']

            # Character stats
            self.health = self.max_health
            self.action_points = self.max_action_points
            self.level = 1
            self.experience = 0.0
            self.nextLevel = 100.0
            self.damage = 0


    def is_enemy(self):
        return self.__class__.__name__ == "Enemy"

    # Add image to the character
    def add_image(self):
        # Get the rect from the resized image
        self.rect = pygame.Rect(self.x, self.y, 30, 40)

    # Load UI for the character
    def loadUI(self, profile: pygame.Surface, health_bar: pygame.Surface, action_points: pygame.Surface):
        self.profile = profile
        self.health_bar = health_bar
        self.action_points_bar = action_points
        self.health_bar_width = self.health_bar.get_width()
        self.action_points_bar_height = self.action_points_bar.get_height()
        print(self.health_bar_width, self.action_points_bar_height)

    def loadAnimations(self, animations: dict):
        self.idle = animations['idle']
        self.walkRight = animations['move_right']
        self.walkLeft = animations['move_right']
        self.attack = animations['attack']
        self.death = animations['dead']
        self.damageTaken = animations['hit']

    def take_damage(self, damage):
        if self.character_state.value != CharacterState.inactive.value:
            self.damage = damage
            self.health -= damage
            if self.health <= 0:
                self.health = 0
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

    def draw_ui(self, window, profile_frame, death_frame, health_bar_frame, action_points_frame, offset):

        # calculate the health and action points percentage
        health_percentage = self.health / self.max_health
        action_points_percentage = self.action_points / self.max_action_points

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
        health_text = font.render(str(self.health), True, (217, 15, 30))
        # health_text = pygame.transform.rotate(health_text, 45)
        window.blit(health_text, (offset - 15, 48))

        # Action points value
        action_points_text = font.render(str(self.action_points), True, (255, 200, 37))
        window.blit(action_points_text, (offset - 22, 35))

        if self.character_state.value >= CharacterState.dead.value:
            window.blit(death_frame, (offset, 0))

    def draw_damage(self, window):
        font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 16)
        damage_text = font.render('-' + str(self.damage), True, (255, 0, 0))
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
            self.moving_right_direction = self.__class__ != "Enemy"
            self.moving_left_direction = self.__class__ == "Enemy"
            self.previous_battle_state = self.battle_state
            self.battle_state = CharacterBattleState.back_in_position
