from turn_based_game.Actor import Actor
from turn_based_game.CharacterController import CharacterController


class Character(Actor):

    def __init__(self, config_file: str, character_name: str, x: int = 200, y: int = 100):
        # Character States
        super().__init__(config_file, character_name, x, y)
        self.controller = CharacterController(self, x, y)
        self.weapon = None
        self.helmet = None
        self.breastplate = None
        self.boots = None

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.strength += 1
        self.defense += 1
        self.max_action_points += 5
        self.action_points = self.max_action_points

    def gain_experience(self, experience):
        self.experience += experience
        if self.experience >= self.nextLevel:
            self.level_up()
            self.nextLevel += 100 * self.level
            return True
        return False

    def play(self, window, adjusted_rect=None, collisions=None):
        self.controller.controller(window, adjusted_rect, collisions)
