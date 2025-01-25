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
class VFX:

    skills = {
        'DARK': [f"turn_based_game/assets/VFX/Dark/Effect_3/Dark_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Dark/Effect_3"))],
        'FIRE': [f"turn_based_game/assets/VFX/Fire/Effect_2/Fire_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Fire/Effect_2"))],
        'ICE': [f"turn_based_game/assets/VFX/Ice/Effect_1/Ice_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Ice/Effect_1"))],
        'LIGHT': [f"turn_based_game/assets/VFX/Light/Effect_2/Light_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Light/Effect_2"))],
        'MAGIC': [f"turn_based_game/assets/VFX/Magic/Effect_1/Magic_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Magic/Effect_1"))],
        'SLASH': [f"turn_based_game/assets/VFX/Physical/Effect_2/Physical_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Physical/Effect_2"))],
        'PIERCE': [f"turn_based_game/assets/VFX/Physical/Effect_1/Physical_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Physical/Effect_1"))],
        'WIND': [f"turn_based_game/assets/VFX/Wind/Effect_3/Wind_Effect_{i}.png" for i in range(1, count_files_in_folder("turn_based_game/assets/VFX/Wind/Effect_3"))]
    }