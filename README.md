
https://github.com/user-attachments/assets/b758c2a0-fadf-4997-95a2-6dc5d5eec4a5
Valebound is a small, incomplete prototype inspired by classic turn-based strategy/adventure games. This repository contains a playable demo focused on core mechanics: overworld movement, enemy encounters, one combat flow and basic equipment/inventory visuals.

## Table of Contents

1. [Features](#features)
2. [Controls](#controls)
3. [Installation](#installation)
   - [Requirements](#requirements)
   - [Running the game](#running-the-game)
4. [Project structure](#project-structure)
5. [State of the game and future plans](#state-of-the-game-and-future-plans)
   - [Known issues](#known-issues)
   - [Roadmap](#roadmap)
## Features
### Start
Player is being spawned on the map with party of 4 characters.  
<img width="1282" height="752" alt="image" src="https://github.com/user-attachments/assets/21fa677a-ea48-4ee8-a5dc-7d13a173a464" />
### Loot
On the map player can find chests with loot:
   - Common Chest (common loot: 75%, rare: 20%, legendary: 5%): <img width="48" height="32" alt="Common_Chest_1" src="https://github.com/user-attachments/assets/ec53c261-a6b2-437b-8986-32de84c2fdb6" />
   - Equipment Chest (common loot: 25%, rare: 65%, legendary: 10%): <img width="48" height="32" alt="Equipment_Chest_1" src="https://github.com/user-attachments/assets/d30093df-8cba-4dc4-a69e-2c2511550d24" />
   - Legendary Chest (common loot: 15%, rare: 55%, legendary: 30%): <img width="48" height="32" alt="Legendary_Chest_1" src="https://github.com/user-attachments/assets/ceccafc3-5574-4b0e-b33d-8e93978fc912" />
  
Each item has a frame indicating its rarity:
   - Common: <img width="16" height="16" alt="common_frame" src="https://github.com/user-attachments/assets/216ec347-252c-4d97-b6b6-a4a3e24af8d5" />
   - Rare: <img width="16" height="16" alt="rare_frame" src="https://github.com/user-attachments/assets/1dd4f09a-ad8d-4bcb-9129-7ee0940f4a85" />
   - Legendary: <img width="16" height="16" alt="legendary_frame" src="https://github.com/user-attachments/assets/4e331a89-e8ab-4324-a6ef-c6165e420d08" />
Upon breaking a chest, loot drops from it, which can be equipped in the inventory.
![inventory](https://github.com/user-attachments/assets/c0cbf4fb-1e70-4902-a687-8d1da3f1ce51)
### Enemy encounters
After looting some chests you can engage in a fight
 - If you approach the enemy first, your team will start.
 - Otherwise, the enemy team will start.
![attack](https://github.com/user-attachments/assets/228964f4-f17e-4428-a605-8f8093ee3b08)
Be careful, as enemies can also attack you if you get too close.
![enemy_attack](https://github.com/user-attachments/assets/33823521-f851-4317-975f-08edb5c49a26)
### Combat
In combat, you can use a basic attack or skills that require a certain amount of action points (AP).
 - You can see HP and AP indicators, as well as information about whose turn it is and who will act next.
![combat](https://github.com/user-attachments/assets/f011ab6b-972d-495d-98da-2ce2b17d36d3)
### Rewards and Defeat
If you win, you will gain XP, and your characters’ stats will increase upon leveling up.
If you lose, the game will end with a Game Over screen, after which the game will close.
No reviving skill has been implemented yet. However, if one of your characters is defeated, they will be automatically revived with 1 HP after winning the battle.
## Controls
### Overworld
  - Arrow keys — move the player around the map
  - Space — attempt melee attack / interact
  - I — open inventory
### Combat
  - Arrow keys — select a target or menu option
  - D — open skill list
  - Enter — confirm/activate selected skill
  - Space — basic attack
## Installation
### Requirements
  - Python 3.12+
  - Pygame 2.6.1+
  ```bash
        python -m pip install --upgrade pip
        python -m pip install pygame==2.6.1
  ```
### Running the game
  From the project root run:  
  ```
  python main.py
  ```
## Project structure
<img width="264" height="358" alt="image" src="https://github.com/user-attachments/assets/a90cd3ae-c3c2-44af-832d-11d3a4f1a4bc" /> 

  
## State of the game and future plans
### Known issues
   - Only the first level is implemented.
   - Only equipment use is implemented; generic items are not functional yet.
   - Enemy AI and combat depth are in prototype stage.
### Roadmap
 - Implementing additional levels and a save system
 - Adding full item effects and consumables
 - Improving combat AI and balancing
 - Polishing UI layout and input mappings
