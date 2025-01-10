import os

import pygame

from turn_based_game.Character import Character
from turn_based_game.Enemy import Enemy

def count_files_in_folder(folder_path):
    # List all items in the folder
    items = os.listdir(folder_path)
    # Filter the list to include only files
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
    # Return the count of files
    return len(files)

def resize_images(image_list, size):# Resize all images in a list to a consistent size
    return [pygame.transform.scale(img, size) for img in image_list]

def character_init_warrior(x:int, y:int):
    character = Character('turn_based_game/config/config.json', 'warrior', x, y)
    size = (64, 48)  # DefWine a consistent size for all images

    # Load animations for the warrior character
    move_right = ['turn_based_game/assets/Characters/Warrior/Individual Sprite/Run/Warrior_Run_' + str(i) + '.png' for i in range(1, 9)]
    idle = ['turn_based_game/assets/Characters/Warrior/Individual Sprite/Idle/Warrior_Idle_' + str(i) + '.png' for i in range(1, 7)]
    attack = ['turn_based_game/assets/Characters/Warrior/Individual Sprite/Attack/Warrior_Attack_' + str(i) + '.png' for i in range(1, 13)]
    hit = ['turn_based_game/assets/Characters/Warrior/Individual Sprite/Hit/Warrior_Hit_' + str(i) + '.png' for i in range(1, 7)]
    dead = ['turn_based_game/assets/Characters/Warrior/Individual Sprite/Dead/Warrior_Death_' + str(i) + '.png' for i in range(1, 7)]

    # Load UI images
    health_bar = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Value.png')
    action_points_bar = pygame.image.load('turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Value.png')
    profile_picture = resize_images([pygame.image.load('turn_based_game/assets/UI/Frames/Characters/Warrior_Profile.png')], (40, 43))[0]

    # Resize the UI images
    move_right = resize_images([pygame.image.load(img) for img in move_right], size)
    idle = resize_images([pygame.image.load(img) for img in idle], size)
    attack = resize_images([pygame.image.load(img) for img in attack], size)
    hit = resize_images([pygame.image.load(img) for img in hit], size)
    dead = resize_images([pygame.image.load(img) for img in dead], size)

    character.loadWalkRightAnimation(move_right)
    character.loadWalkLeftAnimation(move_right)
    character.loadIdleAnimation(idle)
    character.loadAttackAnimation(attack)
    character.loadDamageTakenAnimation(hit)
    character.loadDeathAnimation(dead)
    character.add_image(idle[0])
    character.loadUI(profile_picture, health_bar, action_points_bar)

    return character

def character_init_wizard():

    character = Character('turn_based_game/config/config.json', 'wizard', 150, 105)
    size = (40, 40)  # Define a consistent size for all images

    # Load animations for the wizard character
    move_right = ['turn_based_game/assets/Characters/Wizard/Run/Wizard_Run_' + str(i) + '.png' for i in range(1, 9)]
    idle = ['turn_based_game/assets/Characters/Wizard/Idle/Wizard_Idle_' + str(i) + '.png' for i in range(1, 5)]
    attack = ['turn_based_game/assets/Characters/Wizard/Attack/Wizard_Attack_' + str(i) + '.png' for i in range(1, 14)]
    hit = ['turn_based_game/assets/Characters/Wizard/Hit/Wizard_Hit_' + str(i) + '.png' for i in range(1, 4)]
    dead = ['turn_based_game/assets/Characters/Wizard/Dead/Wizard_Dead_' + str(i) + '.png' for i in range(1, 12)]

    move_right = resize_images([pygame.image.load(img) for img in move_right], size)
    idle = resize_images([pygame.image.load(img) for img in idle], size)
    attack = resize_images([pygame.image.load(img) for img in attack], size)
    hit = resize_images([pygame.image.load(img) for img in hit], size)
    dead = resize_images([pygame.image.load(img) for img in dead], size)

    # Load UI images
    health_bar = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Value.png')
    action_points_bar = pygame.image.load('turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Value.png')
    profile_picture = resize_images([pygame.image.load('turn_based_game/assets/UI/Frames/Characters/Wizard_Profile.png')], (40, 43))[0]

    character.loadWalkRightAnimation(move_right)
    character.loadWalkLeftAnimation(move_right)
    character.loadIdleAnimation(idle)
    character.loadAttackAnimation(attack)
    character.loadDamageTakenAnimation(hit)
    character.loadDeathAnimation(dead)
    character.add_image(idle[0])
    character.loadUI(profile_picture, health_bar, action_points_bar)

    return character

def character_init_healer():

    character = Character('turn_based_game/config/config.json', 'healer', 100, 105)
    size = (64, 64)  # Define a consistent size for all images

    # Load animations for the wizard character
    move_right = ['turn_based_game/assets/Characters/Witch/Run/Witch_Run_' + str(i) + '.png' for i in range(1, 9)]
    idle = ['turn_based_game/assets/Characters/Witch/Idle/Witch_Idle_' + str(i) + '.png' for i in range(1, 7)]
    attack = ['turn_based_game/assets/Characters/Witch/Attack/Witch_Attack_' + str(i) + '.png' for i in range(1, 10)]
    hit = ['turn_based_game/assets/Characters/Witch/Hit/Witch_Hit_' + str(i) + '.png' for i in range(1, 4)]
    dead = ['turn_based_game/assets/Characters/Witch/Dead/Witch_Dead_' + str(i) + '.png' for i in range(1, 13)]

    # Load UI images
    health_bar = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Value.png')
    action_points_bar = pygame.image.load('turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Value.png')
    profile_picture = resize_images([pygame.image.load('turn_based_game/assets/UI/Frames/Characters/Witch_Profile.png')], (40, 43))[0]

    move_right = [pygame.image.load(img) for img in move_right]
    idle = [pygame.image.load(img) for img in idle]
    attack = [pygame.image.load(img) for img in attack]
    hit = [pygame.image.load(img) for img in hit]
    dead = [pygame.image.load(img) for img in dead]

    character.loadWalkRightAnimation(move_right)
    character.loadWalkLeftAnimation(move_right)
    character.loadIdleAnimation(idle)
    character.loadAttackAnimation(attack)
    character.loadDamageTakenAnimation(hit)
    character.loadDeathAnimation(dead)
    character.add_image(idle[0])
    character.loadUI(profile_picture, health_bar, action_points_bar)

    return character

def character_init_archer():

    character = Character('turn_based_game/config/config.json', 'archer', 0, 75)
    size = (64, 64)  # Define a consistent size for all images

    # Load animations for the wizard character
    move_right = ['turn_based_game/assets/Characters/Archer/Run/Archer_Run_' + str(i) + '.png' for i in range(1, 9)]
    idle = ['turn_based_game/assets/Characters/Archer/Idle/Archer_Idle_' + str(i) + '.png' for i in range(1, 9)]
    attack = ['turn_based_game/assets/Characters/Archer/Attack/Archer_Attack_' + str(i) + '.png' for i in range(1, 15)]
    hit = ['turn_based_game/assets/Characters/Archer/Hit/Archer_Hit_' + str(i) + '.png' for i in range(1, 4)]
    dead = ['turn_based_game/assets/Characters/Archer/Dead/Archer_Dead_' + str(i) + '.png' for i in range(1, 25)]

    # Load UI images
    health_bar = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Value.png')
    action_points_bar = pygame.image.load('turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Value.png')
    profile_picture = resize_images([pygame.image.load('turn_based_game/assets/UI/Frames/Characters/Archer_Profile.png')], (40, 43))[0]

    move_right = [pygame.image.load(img) for img in move_right]
    idle = [pygame.image.load(img) for img in idle]
    attack = [pygame.image.load(img) for img in attack]
    hit = [pygame.image.load(img) for img in hit]
    dead = [pygame.image.load(img) for img in dead]

    character.loadWalkRightAnimation(move_right)
    character.loadWalkLeftAnimation(move_right)
    character.loadIdleAnimation(idle)
    character.loadAttackAnimation(attack)
    character.loadDamageTakenAnimation(hit)
    character.loadDeathAnimation(dead)
    character.add_image(idle[0])
    character.loadUI(profile_picture, health_bar, action_points_bar)

    return character

def character_init_enemy(enemy_name:str, x:int, y:int, main_character:Character):

    enemy = Enemy('turn_based_game/config/enemyConfig.json', enemy_name, x, y, main_character)

    size = (64, 64)  # Define a consistent size for all images

    move_right = ['turn_based_game/assets/Enemies/' + enemy_name + '/Run/' + enemy_name + '_Run_' + str(i) + '.png' for i in range(1, count_files_in_folder('turn_based_game/assets/Enemies/' + enemy_name + '/Run/') + 1)]
    idle = ['turn_based_game/assets/Enemies/' + enemy_name + '/Idle/' + enemy_name + '_Idle_' + str(i) + '.png' for i in range(1, count_files_in_folder('turn_based_game/assets/Enemies/' + enemy_name + '/Idle/') + 1)]
    attack = ['turn_based_game/assets/Enemies/' + enemy_name + '/Attack/' + enemy_name + '_Attack_' + str(i) + '.png' for i in range(1, count_files_in_folder('turn_based_game/assets/Enemies/' + enemy_name + '/Attack/') + 1)]
    hit = ['turn_based_game/assets/Enemies/' + enemy_name + '/Hit/' + enemy_name + '_Hit_' + str(i) + '.png' for i in range(1, count_files_in_folder('turn_based_game/assets/Enemies/' + enemy_name + '/Hit/') + 1)]
    dead = ['turn_based_game/assets/Enemies/' + enemy_name + '/Dead/' + enemy_name + '_Dead_' + str(i) + '.png' for i in range(1, count_files_in_folder('turn_based_game/assets/Enemies/' + enemy_name + '/Dead/') + 1)]

    move_right = [pygame.image.load(img) for img in move_right]
    idle = [pygame.image.load(img) for img in idle]
    attack = [pygame.image.load(img) for img in attack]
    hit = [pygame.image.load(img) for img in hit]
    dead = [pygame.image.load(img) for img in dead]

    health_bar = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Value.png')
    action_points_bar = pygame.image.load('turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Value.png')
    profile_picture = resize_images([pygame.image.load('turn_based_game/assets/UI/Frames/Enemies/'+enemy_name+'_Profile.png')], (40, 43))[0]

    enemy.loadWalkRightAnimation(move_right)
    enemy.loadWalkLeftAnimation(move_right)
    enemy.loadIdleAnimation(idle)
    enemy.loadAttackAnimation(attack)
    enemy.loadDamageTakenAnimation(hit)
    enemy.loadDeathAnimation(dead)
    enemy.add_image(idle[0])

    enemy.loadUI(profile_picture, health_bar, action_points_bar)

    return enemy