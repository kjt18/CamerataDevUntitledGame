import unittest
from typing import Optional

import tcod
from tcod import event

from actions import Action, BumpAction

from input_handlers import EventHandler

class TestInputs(unittest.TestCase):
    def setUp(self):
        self.input_handlers = EventHandler()

class test_ev_kydown(TestInputs):
    def test_ev_keydown(self):
        action = BumpAction(dx=0, dy=0)

       # key = event.sym
        key = tcod.event.K_UP
        self.assertEquals(action, BumpAction(dx=0, dy=0))
