from components.ai import HostileEnemy
# from components import consumable
from components import consumable, equippable
from components.equipment import Equipment
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Actor, Item

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=50, base_defense=2, base_power=5),
    inventory=Inventory(capacity=26),
)

orc = Actor(
    char="O",
    color=(5, 60, 5),
    name="Orc",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=11, base_defense=1, base_power=4),
    inventory=Inventory(capacity=0),
    points=200,
)
troll = Actor(
    char="T",
    color=(5, 60, 5),
    name="Troll",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=20, base_defense=2, base_power=5),
    inventory=Inventory(capacity=0),
    points=300,
)
skeleton = Actor(
    char="S",
    color=(5, 60, 5),
    name="Skeleton",
    ai_cls=HostileEnemy,
    equipment=Equipment(),
    fighter=Fighter(hp=5, base_defense=0, base_power=3),
    inventory=Inventory(capacity=0),
    points=100,
)
confusion_scroll = Item(
    char="~",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=10),
    points=150
)
fireball_scroll = Item(
    char="~",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=12, radius=3),
    points=150
)
health_potion = Item(
    char="g",
    color=(42, 252, 10),
    name="Health Potion",
    consumable=consumable.HealingConsumable(amount=4),
    points=50
)
lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
    points=150
)
dagger = Item(
    char="/", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger(), points=175
)
sword = Item(
    char="/", color=(0, 191, 255), name="Sword", equippable=equippable.Sword(), points=225
)
axe = Item(
    char="/", color=(0, 191, 255), name="Axe", equippable=equippable.Axe(), points=250
)
# needle_of_fate = Item(char="/", color=(0, 191, 255), name="NeedleOfFate", equippable=equippable.NeedleOfFate()
# )

leather_armor = Item(
    char="[",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
    points=75
)
chain_mail = Item(
    char="[", color=(139, 69, 19), name="Chain Mail", equippable=equippable.ChainMail(), points=215
)
# needle_of_fate = Item(
#     char="n",
#     color=(42, 252, 10),
#     name="Needle of Fate",
#     consumable=consumable.NeedleDamageConsumable(damage=1337, maximum_range=1),
# )
# sword = Item(
#     char="s",
#     color=(42, 252, 10),
#     name="Sword",
#     consumable=consumable.SwordConsumable(damage=20, maximum_range=1),
# )
# axe = Item(
#     char="a",
#     color=(42, 252, 10),
#     name="Axe",
#     consumable=consumable.AxeConsumable(damage=30, maximum_range=1),
# )
