from components.ai import HostileEnemy
from components import consumable
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item


player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=50, defense=2, power=15),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="O",
    color=(5, 60, 5),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=3),
    inventory=Inventory(capacity=0),
)
troll = Actor(
    char="T",
    color=(5, 60, 5),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defense=1, power=4),
    inventory=Inventory(capacity=0),
)
confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
)
health_potion = Item(
    char="g",
    color=(42, 252, 10),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)
needle_of_fate = Item(
    char="n",
    color=(207, 63, 255),
    name="Needle of Fate",
    consumable=consumable.NeedleDamageConsumable(damage=500, maximum_range=1),
)
sword = Item(
    char="s",
    color=(207, 63, 255),
    name="Sword",
    consumable=consumable.SwordConsumable(damage=20, maximum_range=1),
)
axe = Item(
    char="a",
    color=(207, 63, 255),
    name="Axe",
    consumable=consumable.AxeConsumable(damage=30, maximum_range=1),
)