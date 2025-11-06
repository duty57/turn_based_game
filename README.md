# Valebound
Valebound is a small, incomplete prototype inspired by classic turn-based strategy/adventure games. This repository contains a playable demo focused on core mechanics: overworld movement, enemy encounters, one combat flow and basic equipment/inventory visuals.

## Table of Contents

1. [Features](#features)
2. [Controls](#controls)
3. [Installation](#installation)
   - [Requirements](#requireents)
   - [Running the game](#running-the-game)
4. [Project structure](#project-structure)
5. [State of the game and future plans](#state-of-the-game)
   - [Known issues](#known-issues)
   - [Roadmap](#roadmap)
## Features
   - 2D turn‑based gameplay with a pseudo open world.
   - Random enemy encounters and simple AI (enemies can approach and attack if too close).
   - Lootable chests placed in the world.
   - Inventory/equipment UI (equipment usable; some item types not implemented).
   - Simple animations for characters and enemies, VFX and map tiles.
## Controls
   - [Overworld](#overworld)
     - Arrow keys — move the player around the map
     - Space — attempt melee attack / interact
     - I — open inventory
   - [Combat](#combat)
     - Arrow keys — select a target or menu option
     - D — open skill list
     - Enter — confirm/activate selected skill
     - Space — basic attack
## Installation
### Requirements
  - Python 3.12+
  - Pygame 2.6.1+
  ```bash
        python -m venv .venv
        #Windows
        .venv\Scripts\activate
        # macOS / Linux
        source .venv/bin/activate
  
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
