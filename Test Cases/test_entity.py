import unittest
from unittest.mock import Mock
from components.ai import BaseAI
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from game_map import GameMap

from entity import Actor


class TestActor(unittest.TestCase):
    def setUp(self):
        self.ai = Mock(spec=BaseAI)
        self.fighter = Mock(spec=Fighter)
        self.inventory = Mock(spec=Inventory)
        self.equipment = Mock(spec=Equipment)

    def test_actor_creation(self):
        actor = Actor(
            x=1,
            y=2,
            char='@',
            color=(255, 255, 255),
            name='Player',
            ai_cls=self.ai,
            fighter=self.fighter,
            inventory=self.inventory,
            equipment=self.equipment,
        )

        self.assertEqual(actor.x, 1)
        self.assertEqual(actor.y, 2)
        self.assertEqual(actor.char, '@')
        self.assertEqual(actor.color, (255, 255, 255))
        self.assertEqual(actor.name, 'Player')
        # self.assertIsInstance(actor.ai, BaseAI)
        self.assertEqual(actor.fighter, self.fighter)
        self.assertEqual(actor.inventory, self.inventory)
        self.assertTrue(actor.is_alive)

    def test_actor_is_alive(self):
        actor = Actor(
            x=1,
            y=2,
            char='@',
            color=(255, 255, 255),
            name='Player',
            ai_cls=self.ai,
            fighter=self.fighter,
            inventory=self.inventory,
            equipment=self.equipment,
        )

        self.assertTrue(actor.is_alive)

        actor.ai = None

        self.assertFalse(actor.is_alive)



if __name__ == '__main__':
    unittest.main()
