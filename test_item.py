import unittest
from components.ai import BaseAI
from components.consumable import Consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item


class TestActor(unittest.TestCase):
    def test_init(self):
        ai = BaseAI()
        fighter = Fighter(hp=10, defense=2, power=5)
        inventory = Inventory(capacity=5)
        actor = Actor(x=1, y=2, char="@", name="player", ai_cls=BaseAI, fighter=fighter, inventory=inventory)
        self.assertEqual(actor.x, 1)
        self.assertEqual(actor.y, 2)
        self.assertEqual(actor.char, "@")
        self.assertEqual(actor.name, "player")
        self.assertEqual(actor.ai.__class__, ai.__class__)
        self.assertEqual(actor.fighter.__class__, fighter.__class__)
        self.assertEqual(actor.inventory.__class__, inventory.__class__)
        self.assertEqual(actor.is_alive, True)

    def test_is_alive(self):
        ai = BaseAI()
        fighter = Fighter(hp=10, defense=2, power=5)
        inventory = Inventory(capacity=5)
        actor = Actor(x=1, y=2, char="@", name="player", ai_cls=BaseAI, fighter=fighter, inventory=inventory)
        self.assertEqual(actor.is_alive, True)
        actor.ai = None
        self.assertEqual(actor.is_alive, False)


class TestItem(unittest.TestCase):
    def test_init(self):
        consumable = Consumable(use_function=None)
        item = Item(x=3, y=4, char="!", name="potion", consumable=consumable)
        self.assertEqual(item.x, 3)
        self.assertEqual(item.y, 4)
        self.assertEqual(item.char, "!")
        self.assertEqual(item.name, "potion")
        self.assertEqual(item.consumable.__class__, consumable.__class__)
