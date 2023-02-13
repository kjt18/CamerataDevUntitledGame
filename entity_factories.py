from components.ai import HostileEnemy
from components.consumable import HealingConsumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item


player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=50, defense=2, power=5),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="Orc",
    color=(5, 60, 5),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
)
troll = Actor(
    char="Troll",
    color=(5, 60, 5),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
)

health_potion = Item(
    char="g",
    color=(42, 252, 10),
    name="Health Potion",
    consumable=HealingConsumable(amount=4),
)