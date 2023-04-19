import unittest
from unittest.mock import MagicMock
from components.inventory import Inventory
from entity import Actor, Item
from game_map import GameMap
from message_log import MessageLog

class TestInventory(unittest.TestCase):
    def setUp(self):
        # Create a mock Actor for the parent entity
        self.actor = MagicMock(spec=Actor)
        self.actor.x = 0
        self.actor.y = 0
        self.item = MagicMock(spec=Item)
        self.item.name = "Test Item"
        # Create a mock MessageLog
        self.message_log = MagicMock(spec=MessageLog)
        # Create a mock GameMap
        self.gamemap = MagicMock(spec=GameMap)

        # Create an Inventory with a capacity of 5
        self.inventory = Inventory(5)
        self.inventory.parent = self.actor
        self.inventory.engine.message_log = self.message_log

    def test_inventory_creation(self):
        # Test that the inventory is created with the correct capacity
        self.assertEqual(self.inventory.capacity, 5)
        self.assertEqual(len(self.inventory.items), 0)

    def test_inventory_drop(self):

        # Add the item to the inventory
        self.inventory.items.append(self.item)

        # Call the drop method
        self.inventory.drop(self.item)

        # Test that the item was removed from the inventory
        self.assertNotIn(self.item, self.inventory.items)

        # Test that a message was added to the message log
        self.message_log.add_message.assert_called_once_with("You dropped the Test Item.")

        # Test that the item was placed on the game map at the actor's location
        self.item.place.assert_called_once_with(self.actor.x, self.actor.y, self.gamemap)

        #dropping item on the game map: test manually

if __name__ == '__main__':
    unittest.main()
