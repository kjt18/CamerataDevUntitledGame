import unittest
from unittest.mock import MagicMock

import entity_factories
from components.equipment import Equipment
from components.equippable import Dagger
from components.fighter import Fighter
from entity import Actor

class EquippableTests(unittest.TestCase):
    def setUp(self):
        #Create a mock fighter object for testing
        self.mockActor = MagicMock(spec=Actor)
        self.mockFighter = Fighter(hp=10, base_defense=2, base_power=3)
        self.mockFighter.parent = self.mockActor
        self.mockActor.fighter = self.mockFighter
        self.mockActor.equipment = None

        self.mockEnemyActor = MagicMock(spec=Actor)
        self.mockEnemyActor = entity_factories.skeleton
    def test_weapon(self):
        #Instantiate an equippable item for testing
        testDagger = entity_factories.dagger
        equipment = Equipment()

        equipment.parent = self.mockActor
        self.assertIsNone(equipment.weapon)

        #Test equipping a weapon
        equipment.equip_to_slot("weapon", testDagger, add_message=False)
        self.assertEqual(equipment.weapon, testDagger)
        self.assertTrue(equipment.item_is_equipped(testDagger))

        #test damage boost from dagger
        self.assertEqual(equipment.power_bonus, 1)

        #Test unequipping weapon
        equipment.unequip_from_slot("weapon", testDagger)
        self.assertIsNone(equipment.weapon)

        self.mockFighter
    def test_armor(self):
        # Instantiate an equippable item for testing
        testLeatherArmor = entity_factories.leather_armor
        equipment = Equipment()

        equipment.parent = self.mockActor
        self.assertIsNone(equipment.armor)

        # Test equipping armor
        equipment.equip_to_slot("armor", testLeatherArmor, add_message=False)
        self.assertEqual(equipment.armor, testLeatherArmor)
        self.assertTrue(equipment.item_is_equipped(testLeatherArmor))

        # test defense boost from leather armor
        self.assertEqual(equipment.defense_bonus, 1)

        # Test unequipping armor
        equipment.unequip_from_slot("armor", testLeatherArmor)
        self.assertIsNone(equipment.weapon)

if __name__ == '__main__':
    unittest.main()
