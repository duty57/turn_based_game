import os
from dataclasses import dataclass
import pygame

from turn_based_game.Enums import CharacterState


def count_files_in_folder(folder_path):
    # List all items in the folder
    items = os.listdir(folder_path)
    # Filter the list to include only files
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
    # Return the count of files
    return len(files) + 1


def draw_ui(window, actor, offset):
    profile_frame = GameUI.profile_frame
    health_bar_frame = GameUI.health_bar_frame
    action_points_frame = GameUI.action_points_bar_frame
    death_frame = GameUI.death_frame

    # calculate the health and action points percentage
    health_percentage = max(0, actor.health) / actor.max_health
    action_points_percentage = max(0, actor.action_points) / actor.max_action_points

    # scale the health bar and action points bar
    scaled_health_bar = pygame.transform.scale(GameUI.health_bar, (  # change it to ui health bar
        int(actor.health_bar_width * health_percentage), GameUI.health_bar.get_height()))
    scaled_action_points_bar = pygame.transform.scale(GameUI.action_points_bar, (
        GameUI.action_points_bar.get_width(), int(actor.action_points_bar_height * action_points_percentage)))

    # adjust the position of the action points bar
    adjust_action_points_bar = max(0, actor.action_points_bar_height - scaled_action_points_bar.get_height()) - 1

    # draw the UI elements
    window.blit(profile_frame, (offset, 0))  # profile frame
    window.blit(actor.profile, (offset + 5, 5))  # profile
    window.blit(health_bar_frame, (offset + 10, 50))  # health bar frame
    window.blit(scaled_health_bar, (offset + 13, 53))  # health bar
    window.blit(action_points_frame, (offset - 12, 5))  # action points frame
    window.blit(scaled_action_points_bar, (offset - 9, 5 + adjust_action_points_bar))  # action points bar

    font = pygame.font.Font('turn_based_game/assets/UI/Fonts/Raleway-MediumItalic.ttf', 12)

    # Health value
    health_text = font.render(str(actor.health), True, (217, 15, 30))
    window.blit(health_text, (offset - 15, 48))

    # Action points value
    action_points_text = font.render(str(actor.action_points), True, (255, 200, 37))
    window.blit(action_points_text, (offset - 22, 35))

    if actor.controller.character_state.value >= CharacterState.dead.value:
        window.blit(death_frame, (offset, 0))


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
        "common": [pygame.image.load(f'turn_based_game/assets/Chests/CommonChest/Common_Chest_{i}.png') for i in
                   range(1, count_files_in_folder('turn_based_game/assets/Chests/CommonChest'))],
        "equipment": [pygame.image.load(f'turn_based_game/assets/Chests/EquipmentChest/Equipment_Chest_{i}.png') for i
                      in range(1, count_files_in_folder('turn_based_game/assets/Chests/EquipmentChest'))],
        "legendary": [pygame.image.load(f'turn_based_game/assets/Chests/LegendaryChest/Legendary_Chest_{i}.png') for i
                      in range(1, count_files_in_folder('turn_based_game/assets/Chests/LegendaryChest'))],
    }

    item_frame = {
        "common": pygame.image.load('turn_based_game/assets/UI/Frames/Items/common_frame.png'),
        "rare": pygame.image.load('turn_based_game/assets/UI/Frames/Items/rare_frame.png'),
        "legendary": pygame.image.load('turn_based_game/assets/UI/Frames/Items/legendary_frame.png'),
    }
    item_colors = {
        "common": (106, 166, 65),
        "rare": (11, 178, 191),
        "legendary": (236, 106, 14)
    }