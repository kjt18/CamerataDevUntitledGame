"""Handle the loading and initialization of game sessions."""
from __future__ import annotations

import copy
import lzma
import pickle

# from typing import Optional

# import tcod

import color
from engine import Engine
import entity_factories
from game_map import GameMap, GameWorld
import input_handlers


# from procgen import generate_dungeon

# Load the background image and remove the alpha channel.
# background_image = tcod.image.load("menu_background.png")[:, :, :3]


def new_game() -> Engine:
    """Return a brand new game session as an Engine instance."""
    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    player = copy.deepcopy(entity_factories.player)

    engine = Engine(player=player)

    engine.game_world = GameWorld(
        engine=engine,
        max_rooms=max_rooms,
        room_min_size=room_min_size,
        room_max_size=room_max_size,
        map_width=map_width,
        map_height=map_height,
        # max_monsters_per_room=2,
        # max_items_per_room=2,
    )

    engine.game_world.generate_floor()
    engine.update_fov()

    engine.message_log.add_message(
        "Hello, Welcome Adventure to CamerataDevUntitledGame!", color.welcome_text
    )
    return engine
