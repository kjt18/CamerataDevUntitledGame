#class test_inventory:
from components.base_component import BaseComponent
from components.inventory import Inventory
from entity import Actor, Item, Entity
from components.consumable import Consumable

#adding inventory is an Action
def test_drop():
    inventory = Inventory(capacity=10)

    my_consumable = Consumable()

    # Create an Item object with the desired parameters
    item = Item(x=0, y=0, char="?", color=(255, 255, 255), name="<Unnamed>", consumable=my_consumable)
    #item = Item(consumable=None)
    # Test dropping an item from an empty inventory
    inventory.drop(item)
    assert not inventory.items == item



    # Test dropping an item from a non-empty inventory
    inventory.items.append(item)
    inventory.drop(item)
    assert not inventory.items
