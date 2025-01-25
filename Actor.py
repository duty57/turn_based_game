import json

import pygame

# TODO formula for enemy leveling: player_level + 1 * (player_level // 5)
class Actor(pygame.sprite.Sprite):
    def __init__(self, config_file: str, character_name: str, x: int = 200, y: int = 100):
        # Character States
        super().__init__()
        self.rect = pygame.Rect(x, y, 30, 40)
        self.controller = None

        # Read JSON file with character information
        with open(config_file) as file:
            data = json.load(file)
            data = data[character_name]
            self.name = data['name']

            # Character attributes
            self.immunity = data['immunity']
            self.weakness = data['weakness']
            self.element = data['element']
            self.skills = data.get('skills', [])

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
            self.damage = self.strength

    def is_enemy(self):
        return self.__class__.__name__ == 'Enemy'
    # Load UI for the character
    def load_ui(self, profile: pygame.Surface, health_bar: pygame.Surface, action_points: pygame.Surface):
        self.controller.load_ui(profile, health_bar, action_points)

    def load_animations(self, animations: dict):
        self.controller.load_animations(animations)
