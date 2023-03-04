import unittest

from components.fighter import Fighter
from entity import Actor
from components.ai import BaseAI

#ai =
fighter = Fighter(hp=10, defense=2, power=3)
#consumables affect defense and power stats

#Test setting different values for the fighter class
def test_fighter_values():
    parent: Actor

    # Test hp getter
    assert fighter.hp == 10

    # Test hp setter, should set to max
    fighter.hp = 15
    assert fighter.hp == 10

    # Test Fighter.hp setter
    fighter.hp = 5
    assert fighter.hp == 5

    #Test Fighter.hp setter with value less than zero
    #fighter.hp = -5
    #assert fighter.hp == 0

#Test gaining and losing health
def test_fighter_health():

    # Test healing when already at full health, should not go past max
    amount_recovered = fighter.heal(5)
    assert amount_recovered == 0
    assert fighter.hp == 10

    # Test damage
    fighter.take_damage(4)
    assert fighter.hp == 6

    # Test healing
    amount_recovered = fighter.heal(3)
    assert amount_recovered == 3
    assert fighter.hp == 9

    # Test damage greater than current hp, should not be negative
    fighter.take_damage(10)
    assert fighter.hp == 0

