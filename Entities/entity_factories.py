from components.ai import HostileEnemy
from components.fighter import Fighter
from Entities.entity import Actor

player = Actor(
    char="@",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=50, defense=2, power=5),
)

orc = Actor(
    char="Orc",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=0, power=2),
)
troll = Actor(
    char="Troll",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defense=1, power=4),
)