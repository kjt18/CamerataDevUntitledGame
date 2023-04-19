import unittest
from unittest.mock import MagicMock, patch

import components
import entity_factories
from components.equippable import Equippable
from components.fighter import Fighter
from entity import Actor
from equipment_types import EquipmentType
from message_log import MessageLog
from engine import Engine

class TestFighter(unittest.TestCase):
    def setUp(self):

        #Create a mock fighter object for testing
        self.mockActor = MagicMock(spec=Actor)
        self.mockFighter = Fighter(hp=10, base_defense=2, base_power=3)
        self.mockFighter.parent = self.mockActor
        self.mockActor.fighter = self.mockFighter

        self.mockActor.ai = components.ai.HostileEnemy
        self.mockActor.points = 0
        self.mockActor.name = "test"

    #Test setting different values for the fighter class
    def test_fighter_values(self):

        # Test hp getter
        self.assertEqual(self.mockFighter.hp, 10)

        # Test hp setter, should set to max
        self.mockFighter.hp = 15
        self.assertEqual(self.mockFighter.hp, 10)

        # Test Fighter.hp setter
        self.mockFighter.hp = 5
        self.assertEqual(self.mockFighter.hp, 5)

        #test health cannot be set below 0
        self.mockFighter.hp = -1
        self.assertEqual(self.mockFighter.hp, 0)

    #Test gaining and losing health
    def test_fighter_health(self):

        # Test healing when already at full health, should not go past max
        amount_recovered = self.mockFighter.heal(5)
        assert amount_recovered == 0
        assert self.mockFighter.hp == 10

        # Test damage
        self.mockFighter.take_damage(4)
        assert self.mockFighter.hp == 6

        # Test healing
        amount_recovered = self.mockFighter.heal(3)
        assert amount_recovered == 3
        assert self.mockFighter.hp == 9

        #test losing more than current health
        self.mockFighter.take_damage(10)
        self.assertEqual(self.mockFighter.hp, 0)


    def test_defense(self):
        #create mock armor
        mockArmor = MagicMock(spec=Equippable)
        mockArmor.defense_bonus = 2
        mockArmor.equipment_type = EquipmentType.ARMOR
        self.mockActor.equipment = None

        #Test no armor
        self.assertEqual(self.mockFighter.defense, 2)
        self.assertEqual(self.mockFighter.defense_bonus, 0)

        #Test with armor equipped
        self.mockActor.equipment = mockArmor
        self.assertEqual(self.mockFighter.defense, 4)
        self.assertEqual(self.mockFighter.defense_bonus, 2)

    def test_power(self):
        #create mock weapon
        mockWeapon = MagicMock(spec=Equippable)
        mockWeapon.power_bonus = 2
        mockWeapon.equipment_type = EquipmentType.WEAPON
        self.mockActor.equipment = None

        # Test no armor
        self.assertEqual(self.mockFighter.power, 3)
        self.assertEqual(self.mockFighter.power_bonus, 0)

        # Test with armor equipped
        self.mockActor.equipment = mockWeapon
        self.assertEqual(self.mockFighter.power, 5)
        self.assertEqual(self.mockFighter.power_bonus, 2)

if __name__ == '__main__':
    unittest.main()