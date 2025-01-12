import json

import pygame
from Enums import CharacterBattleState, CharacterState

class Character(pygame.sprite.Sprite):

    def __init__(self, configFile: str, CharacterName: str, x: int = 200, y: int = 100):

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

        self.enemy = False

        self.in_battle = False
        self.in_action = False

        # Read JSON file with character information
        with open(configFile) as file:
            data = json.load(file)
            data = data[CharacterName]
            self.name = data['name']

            # Character attributes
            self.immunity = data['immunity']
            self.weakness = data['weakness']
            self.element = data['element']
            self.abilities = data.get('abilities', [])

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

            # Character equipment
            self.head_armor = None
            self.chest_armor = None
            self.shoes = None
            self.weapon = None

            # Character animations
            self.idle = None
            self.walkRight = None
            self.walkLeft = None
            self.attack = None
            self.death = None
            self.damageTaken = None

    # Add image to the character
    def add_image(self):
        # Get the rect from the resized image
        self.rect = pygame.Rect(self.x, self.y, 30, 40)

    # Load UI for the character
    def loadUI(self, profile, health_bar, action_points_bar):
        self.profile = profile
        self.health_bar = health_bar
        self.action_points_bar = action_points_bar
        self.health_bar_width = self.health_bar.get_width()
        self.action_points_bar_height = self.action_points_bar.get_height()

    def loadAnimations(self, animations: dict):
        self.idle = animations['idle']
        self.walkRight = animations['move_right']
        self.walkLeft = animations['move_right']
        self.attack = animations['attack']
        self.death = animations['dead']
        self.damageTaken = animations['hit']

    def level_up(self):
        self.level += 1

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.nextLevel:
            self.level_up()
            self.experience = 0
            self.nextLevel += 100 * self.level

    def take_damage(self, damage):
        if self.character_state.value != CharacterState.inactive.value:
            self.damage = damage
            self.health -= damage
            if self.health < 0:
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

    # Character controller
    def controller(self, keys, collisions=[]):
        if self.character_state != CharacterState.inactive:
            move_x = 0
            move_y = 0
            if not self.in_battle:

                if keys[pygame.K_SPACE] and self.character_class == 'Warrior' and not self.character_state == CharacterState.hit:
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

        if not self.enemy:
            adjusted_rect = adjusted_rect.move(-16, -10)

        if not self.in_battle:
            self.finished_attack = False
            self.finished_hit = False  # maybe here is the problem with hit animations

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
                if self.attackFrameCount >= attackAnimationLength * (30//deathAnimationLength):
                    self.attackFrameCount = 0
                    self.finished_attack = True
                    self.character_state = CharacterState.idle
                    if self.target:
                        self.previous_battle_state = self.battle_state
                        self.battle_state = CharacterBattleState.attacking
                        self.target.collide()
                        self.target.take_damage(30)
            case CharacterState.hit:
                frame_index = (self.hit_frame_count // (hitAnimationLength * 4 // hitAnimationLength)) % hitAnimationLength
                self.draw_damage(window)
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.damageTaken[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.damageTaken[frame_index], adjusted_rect)
                self.hit_frame_count += 1
                if self.hit_frame_count >= hitAnimationLength * (30//deathAnimationLength):
                    self.character_state = CharacterState.idle
                    self.hit_frame_count = 0
                    self.finished_hit = True
            case CharacterState.dead:
                frame_index = (self.deathFrameCount // (deathAnimationLength * 4 // deathAnimationLength)) % deathAnimationLength
                if self.moving_left_direction:
                    window.blit(pygame.transform.flip(self.death[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.death[frame_index], adjusted_rect)
                self.deathFrameCount += 1
                if self.deathFrameCount >= deathAnimationLength * (30//deathAnimationLength):
                    self.character_state = CharacterState.inactive
                    self.deathFrameCount = 0

        self.frameCount += 1
        pygame.draw.rect(window, (255, 0, 0), self.rect, 2)

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
        damage_text = font.render('-'+str(self.damage), True, (255, 0, 0))
        window.blit(damage_text, (self.x, self.y-50))
        # Combat system

    def go_to_enemy(self, enemy):
        if self.x < enemy.rect.x - 20:
            self.moveRight()
        elif self.x > enemy.rect.x + 20:
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
            self.moving_right_direction = True
            self.moving_left_direction = False
            self.previous_battle_state = self.battle_state
            self.battle_state = CharacterBattleState.back_in_position

# TODO: Maybe resize the images(source) to a consistent size
