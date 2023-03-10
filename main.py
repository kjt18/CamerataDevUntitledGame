#!/usr/bin/env python3
import copy
import random
import sys
import traceback
import zerorpc
import tcod

import color
from engine import Engine
import entity_factories
import exceptions
import input_handlers
from procgen import generate_dungeon
import setup_game


class Main:

    def __init__(self):
        # random.seed(sys.argv[1])
        self.main()

    def main(self) -> None:

        self.screen_width = 80
        self.screen_height = 50

        map_width = 80
        map_height = 43

        room_max_size = 10
        room_min_size = 6
        max_rooms = 30

        max_monsters_per_room = 2
        max_items_per_room = 2

        self.tileset = tcod.tileset.load_tilesheet(
            "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        )

        player = copy.deepcopy(entity_factories.player)

        engine = setup_game.new_game()

        engine.game_map = generate_dungeon(
            max_rooms=max_rooms,
            room_min_size=room_min_size,
            room_max_size=room_max_size,
            map_width=map_width,
            map_height=map_height,
            # max_monsters_per_room=max_monsters_per_room,
            # max_items_per_room=max_items_per_room,
            engine=engine,
        )
        engine.update_fov()

        self.handler: input_handlers.BaseEventHandler = input_handlers.MainGameEventHandler(engine)

        self.root_console = tcod.Console(self.screen_width, self.screen_height, order="F")

        self.context = tcod.context.new_terminal(
            self.screen_width,
            self.screen_height,
            tileset=self.tileset,
            title="CamerataDevUntitledGame",
            vsync=True, )
        self.render_console()

    # Use this as a template for all other relevant events
    def move_up(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_UP, tcod.event.K_UP, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    def handle_event(self, event):
        try:
            self.context.convert_event(event)
            self.handler = self.handler.handle_events(event)
        except Exception:  # Handle exceptions in game.
            traceback.print_exc()  # Print error to stderr.
            # Then print the error to the message log.
            if isinstance(self.handler, input_handlers.EventHandler):
                self.handler.engine.message_log.add_message(
                    traceback.format_exc(), color.error
                )

    def render_console(self):
        self.root_console.clear()
        self.handler.on_render(console=self.root_console)


if __name__ == "__main__":
    s = zerorpc.Server(Main())
    s.bind("tcp://0.0.0.0:4242")
    s.run()
