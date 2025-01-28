import pygame

from turn_based_game.Actors.Actor import Actor
from turn_based_game.Controllers.CharacterController import CharacterController
from turn_based_game.Items.Item import Item
from turn_based_game.Items.Armor import Armor
from turn_based_game.Items.Weapon import Weapon


def unequip_item(item: Item):
    character = item.owner
    if character:
        if item.item_type == "weapon":
            character.unequip_weapon()
        elif item.item_type == "helmet":
            character.unequip_helmet()
        elif item.item_type == "chestplate":
            character.unequip_chestplate()


def equip_item(item: Item, character):
    if character:
        if item.item_type == "weapon":
            character.equip_weapon(item)
        elif item.item_type == "helmet":
            character.equip_helmet(item)
        elif item.item_type == "chestplate":
            character.equip_chestplate(item)


class Character(Actor):

    def __init__(self, config_file: str, character_name: str, x: int = 200, y: int = 100):
        # Character States
        super().__init__(config_file, character_name, x, y)
        self.controller = CharacterController(self, x, y)
        self.weapon = None
        self.helmet = None
        self.chestplate = None

    def level_up(self):
        self.level += 1
        self.max_health += 10
        self.health = self.max_health
        self.strength += 1
        self.defense += 1
        self.max_action_points += 5
        self.action_points = self.max_action_points

    def gain_experience(self, experience: int) -> bool:  # returns true if the character levels up
        self.experience += experience
        if self.experience >= self.nextLevel:
            self.level_up()
            self.nextLevel += 100 * self.level
            return True
        return False

    def play(self, window: pygame.Surface, adjusted_rect: pygame.Rect = None, collisions: pygame.Rect = None):
        self.controller.controller(window, adjusted_rect, collisions)

    # Equip and Unequip Items
    def equip_helmet(self, helmet: Armor):
        self.helmet = helmet
        self.defense += helmet.defenseBonus
        self.max_health += helmet.HPBonus
        self.agility += helmet.agilityBonus
        self.max_action_points += helmet.actionPointsBonus

    def equip_chestplate(self, chestplate: Armor):
        self.chestplate = chestplate
        self.defense += chestplate.defenseBonus
        self.max_health += chestplate.HPBonus
        self.agility += chestplate.agilityBonus
        self.max_action_points += chestplate.actionPointsBonus

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        self.strength += weapon.damage
        self.max_health += weapon.HPBonus
        self.max_action_points += weapon.actionPointsBonus

    def unequip_helmet(self):
        self.defense -= self.helmet.defenseBonus
        self.max_health -= self.helmet.HPBonus
        self.agility -= self.helmet.agilityBonus
        self.max_action_points -= self.helmet.actionPointsBonus

        self.reset_stats()
        self.helmet = None

    def unequip_chestplate(self):
        self.defense -= self.chestplate.defenseBonus
        self.max_health -= self.chestplate.HPBonus
        self.agility -= self.chestplate.agilityBonus
        self.max_action_points -= self.chestplate.actionPointsBonus

        self.reset_stats()
        self.chestplate = None

    def unequip_weapon(self):
        self.strength -= self.weapon.damage
        self.max_health -= self.weapon.HPBonus
        self.max_action_points -= self.weapon.actionPointsBonus

        self.reset_stats()
        self.weapon = None

    def reset_stats(self):  # ensures that the stats do not exceed the maximum values
        self.health = min(self.health, self.max_health)
        self.action_points = min(self.action_points, self.max_action_points)
