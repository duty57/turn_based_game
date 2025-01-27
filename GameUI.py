import os
from dataclasses import dataclass
import pygame


def count_files_in_folder(folder_path):
    # List all items in the folder
    items = os.listdir(folder_path)
    # Filter the list to include only files
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
    # Return the count of files
    return len(files) + 1


@dataclass
class GameUI:
    # Load all images for the UI
    health_bar = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Value.png')
    health_bar_frame = pygame.image.load('turn_based_game/assets/UI/HealthBar/HealthBar_Frame.png')
    action_points_bar = pygame.image.load('turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Value.png')
    action_points_bar_frame = pygame.image.load(
        'turn_based_game/assets/UI/ActionPointsBar/ActionPointsBar_Frame.png')

    profile_frame = pygame.image.load('turn_based_game/assets/UI/Frames/Frame.png')
    profile_frame = pygame.transform.scale(profile_frame, (50, 50))
    death_frame = pygame.image.load('turn_based_game/assets/UI/Frames/Dead_Frame.png')
    list_image = pygame.transform.scale(pygame.image.load('turn_based_game/assets/UI/Lists/list_long.png'),
                                        (325, 522))
    character_highlight = pygame.transform.scale(
        pygame.image.load('turn_based_game/assets/VFX/Highlights/Character_highlight.png'), (48, 12))
    enemy_highlight = pygame.transform.scale(
        pygame.image.load('turn_based_game/assets/VFX/Highlights/Enemy_highlight.png'), (48, 12))
    character_frame_highlight = pygame.transform.scale(
        pygame.image.load('turn_based_game/assets/VFX/Highlights/Character_frame_highlight.png'), (50, 50))
    enemy_frame_highlight = pygame.transform.scale(
        pygame.image.load('turn_based_game/assets/VFX/Highlights/Enemy_frame_highlight.png'), (50, 50))

    a_key = pygame.transform.scale(pygame.image.load('turn_based_game/assets/UI/Keys/A.png'), (32, 32))
    d_key = pygame.transform.scale(pygame.image.load('turn_based_game/assets/UI/Keys/D.png'), (32, 32))
    enter_key = pygame.transform.scale(pygame.image.load('turn_based_game/assets/UI/Keys/ENTER.png'), (32, 32))
    space_key = pygame.transform.scale(pygame.image.load('turn_based_game/assets/UI/Keys/SPACE.png'), (64, 32))

    backpack = pygame.image.load('turn_based_game/assets/UI/Inventory/backpack_small.png')

    chests = {
        "common": pygame.image.load('turn_based_game/assets/Chests/CommonChest/Common_Chest_1.png'),
        "equipment": pygame.image.load('turn_based_game/assets/Chests/EquipmentChest/Equipment_Chest_1.png'),
        "legendary": pygame.image.load('turn_based_game/assets/Chests/LegendaryChest/Legendary_Chest_1.png'),
    }

    chest_animation = {
        "common": [pygame.image.load(f'turn_based_game/assets/Chests/CommonChest/Common_Chest_{i}.png') for i in range(1, count_files_in_folder('turn_based_game/assets/Chests/CommonChest'))],
        "equipment": [pygame.image.load(f'turn_based_game/assets/Chests/EquipmentChest/Equipment_Chest_{i}.png') for i in range(1, count_files_in_folder('turn_based_game/assets/Chests/EquipmentChest'))],
        "legendary": [pygame.image.load(f'turn_based_game/assets/Chests/LegendaryChest/Legendary_Chest_{i}.png') for i in range(1, count_files_in_folder('turn_based_game/assets/Chests/LegendaryChest'))],
    }

    item_frame = {
        "common": pygame.image.load('turn_based_game/assets/UI/Frames/Items/common_frame.png'),
        "rare": pygame.image.load('turn_based_game/assets/UI/Frames/Items/rare_frame.png'),
        "legendary": pygame.image.load('turn_based_game/assets/UI/Frames/Items/legendary_frame.png'),
    }
