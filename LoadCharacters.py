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
    return len(files) + 1


def resize_images(image_list, size):  # Resize all images in a list to a consistent size
    return [pygame.transform.scale(img, size) for img in image_list]

def init_character(character_name: str, x: int = 0, y: int = 0, resize: bool = False, size: tuple = (0, 0)):
    character = Character('turn_based_game/config/config.json', character_name, x, y)

    move_right = [
        f'turn_based_game/assets/Characters/{character_name}/Run/{character_name}_Run_{i}.png' for
        i in range(1, count_files_in_folder(f'turn_based_game/assets/Characters/{character_name}/Run/'))]
    idle = [
        f'turn_based_game/assets/Characters/{character_name}/Idle/{character_name}_Idle_{i}.png' for
        i in range(1, count_files_in_folder(f'turn_based_game/assets/Characters/{character_name}/Idle/'))]
    attack = [
        f'turn_based_game/assets/Characters/{character_name}/Attack/{character_name}_Attack_{i}.png' for
        i in range(1, count_files_in_folder(f'turn_based_game/assets/Characters/{character_name}/Attack/'))]
    hit = [
        f'turn_based_game/assets/Characters/{character_name}/Hit/{character_name}_Hit_{i}.png' for
        i in range(1, count_files_in_folder(f'turn_based_game/assets/Characters/{character_name}/Hit/'))]
    dead = [
        f'turn_based_game/assets/Characters/{character_name}/Dead/{character_name}_Dead_{i}.png' for
        i in range(1, count_files_in_folder(f'turn_based_game/assets/Characters/{character_name}/Dead/'))]

    move_right = [pygame.image.load(img) for img in move_right]
    idle = [pygame.image.load(img) for img in idle]
    attack = [pygame.image.load(img) for img in attack]
    hit = [pygame.image.load(img) for img in hit]
    dead = [pygame.image.load(img) for img in dead]

    if resize:
        move_right = resize_images(move_right, size)
        idle = resize_images(idle, size)
        attack = resize_images(attack, size)
        hit = resize_images(hit, size)
        dead = resize_images(dead, size)

    profile_picture = \
    resize_images([pygame.image.load(f'turn_based_game/assets/UI/Frames/Characters/{character_name}_Profile.png')],
                  (40, 43))[0]

    animations_dict = {
        'move_right': move_right,
        'move_left': move_right,  # The character moves left by flipping the right animation
        'idle': idle,
        'attack': attack,
        'hit': hit,
        'dead': dead
    }
    character.load_animations(animations_dict)
    character.load_ui(profile_picture)

    return character


def character_init_enemy(enemy_name: str, x: int, y: int, main_character: Character):
    enemy = Enemy('turn_based_game/config/enemyConfig.json', enemy_name, x, y, main_character)

    size = (64, 64)  # Define a consistent size for all images

    move_right = [f'turn_based_game/assets/Enemies/{enemy_name}/Run/{enemy_name}_Run_{str(i)}.png' for
                  i in range(1, count_files_in_folder(f'turn_based_game/assets/Enemies/{enemy_name}/Run/'))]
    idle = [f'turn_based_game/assets/Enemies/{enemy_name}/Idle/{enemy_name}_Idle_{str(i)}.png' for
                  i in range(1, count_files_in_folder(f'turn_based_game/assets/Enemies/{enemy_name}/Idle/'))]
    attack = [f'turn_based_game/assets/Enemies/{enemy_name}/Attack/{enemy_name}_Attack_{i}.png'
              for i in range(1, count_files_in_folder(f'turn_based_game/assets/Enemies/{enemy_name}/Attack/'))]
    hit = [f'turn_based_game/assets/Enemies/{enemy_name}/Hit/{enemy_name}_Hit_{i}.png'
           for i in range(1, count_files_in_folder(f'turn_based_game/assets/Enemies/{enemy_name}/Hit/'))]
    dead = [f'turn_based_game/assets/Enemies/{enemy_name}/Dead/{enemy_name}_Dead_{i}.png'
            for i in range(1, count_files_in_folder(f'turn_based_game/assets/Enemies/{enemy_name}/Dead/'))]

    move_right = [pygame.image.load(img) for img in move_right]
    idle = [pygame.image.load(img) for img in idle]
    attack = [pygame.image.load(img) for img in attack]
    hit = [pygame.image.load(img) for img in hit]
    dead = [pygame.image.load(img) for img in dead]

    profile_picture = \
    resize_images([pygame.image.load(f'turn_based_game/assets/UI/Frames/Enemies/{enemy_name}_Profile.png')], (40, 43))[0]

    animations_dict = {
        'move_right': move_right,
        'move_left': move_right,  # The character moves left by flipping the right animation
        'idle': idle,
        'attack': attack,
        'hit': hit,
        'dead': dead
    }
    enemy.load_animations(animations_dict)
    enemy.load_ui(profile_picture)

    return enemy
