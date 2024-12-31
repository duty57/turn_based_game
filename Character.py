import json

import pygame


class Character(pygame.sprite.Sprite):

    def __init__(self, configFile: str, CharacterName: str, x: int = 200, y: int = 100):

        #Character States
        super().__init__()
        self.image = None
        self.rect = None

        self.moving_right_direction = True
        self.moving_left_Direction = False
        self.idling = True
        self.attacking = False
        self.is_hit = False

        #Movement
        self.frameCount = 0
        self.attackFrameCount = 0
        self.x = x
        self.y = y

        self.enemy = False

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

            self.maxHealth = data['maxHealth']
            self.strength = data['strength']
            self.intelligence = data['intelligence']
            self.defense = data['defense']
            self.speed = data['speed']
            self.agility = data['agility']
            self.actionPoints = data['actionPoints']

            self.characterClass = data['characterClass']

            # Character stats
            self.health = self.maxHealth
            self.level = 1
            self.experience = 0.0
            self.nextLevel = 100.0

            # Character equipment
            self.HeadArmor = None
            self.ChestArmor = None
            self.Shoes = None
            self.Weapon = None

            # Character animations
            self.idle = None
            self.walkRight = None
            self.walkLeft = None
            self.attack = None
            self.death = None
            self.damageTaken = None


    def add_image(self, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def level_up(self):
        self.level += 1

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.nextLevel:
            self.level_up()
            self.experience = 0
            self.nextLevel += 100 * self.level

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def loadIdleAnimation(self, idle):
        self.idle = idle
    def loadWalkRightAnimation(self, walkRight):
        self.walkRight = walkRight
    def loadWalkLeftAnimation(self, walkLeft):
        self.walkLeft = walkLeft
    def loadAttackAnimation(self, attack):
        self.attack = attack
    def loadDeathAnimation(self, death):
        self.death = death
    def loadDamageTakenAnimation(self, damageTaken):
        self.damageTaken = damageTaken

    def collide(self):
        self.is_hit = True

    def controller(self, keys):
        move_x = 0
        move_y = 0

        self.idling = True

        if keys[pygame.K_LEFT]:
            move_x = -1
            self.moving_left_Direction = True
            self.moving_right_direction = False
            self.idling = False
        elif keys[pygame.K_RIGHT]:
            move_x = 1
            self.moving_left_Direction = False
            self.moving_right_direction = True
            self.idling = False

        if keys[pygame.K_UP]:
            move_y = -1
            self.idling = False
        elif keys[pygame.K_DOWN]:
            move_y = 1
            self.idling = False

        if keys[pygame.K_SPACE] and self.characterClass == 'Warrior' and not self.is_hit:
            self.attacking = True
            self.idling = True


        if move_x != 0 and move_y != 0:
            move_x *= 0.7071  # 1/sqrt(2)
            move_y *= 0.7071  # 1/sqrt(2)

        self.x += move_x * self.speed / 5
        self.y += move_y * self.speed / 5
        self.rect.topleft = (self.x, self.y)


    def draw(self, window, adjusted_rect):

        walkAnimationLength = len(self.walkRight)
        idleAnimationLength = len(self.idle)
        attackAnimationLength = len(self.attack)
        hitAnimationLength = len(self.damageTaken)

        if not self.idling and not self.attacking:
            # moving when not idle
            if self.moving_right_direction:
                frame_index = (self.frameCount // (walkAnimationLength * 4 // walkAnimationLength)) % walkAnimationLength
                window.blit(self.walkRight[frame_index], adjusted_rect)
            elif self.moving_left_Direction:
                frame_index = (self.frameCount // (walkAnimationLength * 4 // walkAnimationLength)) % walkAnimationLength
                window.blit(pygame.transform.flip(self.walkRight[frame_index], True, False), adjusted_rect)
        else:
            #counting the frames for the idle animation
            frame_index = (self.frameCount // (idleAnimationLength * 4 // idleAnimationLength)) % idleAnimationLength

            if self.is_hit:#hit animation if hit is true and idle is true
                #counting the frames for the hit animation
                frame_index = (self.frameCount // (hitAnimationLength * 4 // hitAnimationLength)) % hitAnimationLength
                if self.moving_left_Direction:
                    window.blit(pygame.transform.flip(self.damageTaken[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.damageTaken[frame_index], adjusted_rect)
                self.frameCount += 1
                if self.frameCount >= hitAnimationLength * 4:
                    self.is_hit = False
                    self.frameCount = 0
            elif self.attacking:#attack animation if attack is true and idle is true
                #counting the frames for the attack animation
                frame_index = (self.attackFrameCount // (attackAnimationLength * 2 // attackAnimationLength)) % attackAnimationLength
                if self.moving_left_Direction:
                    window.blit(pygame.transform.flip(self.attack[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.attack[frame_index], adjusted_rect)
                self.attackFrameCount += 1
                if self.attackFrameCount >= attackAnimationLength * 2:
                    self.attacking = False
                    self.attackFrameCount = 0
            else:
                #idle animation when nothing is happening
                if self.moving_left_Direction:
                    window.blit(pygame.transform.flip(self.idle[frame_index], True, False), adjusted_rect)
                else:
                    window.blit(self.idle[frame_index], adjusted_rect)

        self.frameCount += 1
        pygame.display.update()


#TODO: Maybe resize the images(source) to a consistent size