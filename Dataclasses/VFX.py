import os
from dataclasses import dataclass
import pygame


def count_files_in_folder(folder_path: str) -> int:
    # List all items in the folder
    items = os.listdir(folder_path)
    # Filter the list to include only files
    files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
    # Return the count of files
    return len(files) + 1


@dataclass
class VFX:
    # Dictionary of VFX animations for different skills
    skills = {
        'DARK': [f"assets/VFX/Dark/Effect_3/Dark_Effect_{i}.png" for i in
                 range(1, count_files_in_folder("assets/VFX/Dark/Effect_3"))],
        'FIRE': [f"assets/VFX/Fire/Effect_2/Fire_Effect_{i}.png" for i in
                 range(1, count_files_in_folder("assets/VFX/Fire/Effect_2"))],
        'ICE': [f"assets/VFX/Ice/Effect_1/Ice_Effect_{i}.png" for i in
                range(1, count_files_in_folder("assets/VFX/Ice/Effect_1"))],
        'LIGHT': [f"assets/VFX/Light/Effect_2/Light_Effect_{i}.png" for i in
                  range(1, count_files_in_folder("assets/VFX/Light/Effect_2"))],
        'MAGIC': [f"assets/VFX/Magic/Effect_1/Magic_Effect_{i}.png" for i in
                  range(1, count_files_in_folder("assets/VFX/Magic/Effect_1"))],
        'SLASH': [f"assets/VFX/Physical/Effect_2/Physical_Effect_{i}.png" for i in
                  range(1, count_files_in_folder("assets/VFX/Physical/Effect_2"))],
        'PIERCE': [f"assets/VFX/Physical/Effect_1/Physical_Effect_{i}.png" for i in
                   range(1, count_files_in_folder("assets/VFX/Physical/Effect_1"))],
        'WIND': [f"assets/VFX/Wind/Effect_3/Wind_Effect_{i}.png" for i in
                 range(1, count_files_in_folder("assets/VFX/Wind/Effect_3"))]
    }
