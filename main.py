#!/usr/bin/env python3
import copy
import traceback
import tcod
import color

import entity_factories
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

    def move_down(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_DOWN, tcod.event.K_DOWN, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    def move_left(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_LEFT, tcod.event.K_LEFT, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    def move_right(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_RIGHT, tcod.event.K_RIGHT, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    # todo change keycodes
    def move_up_left(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_Y, tcod.event.K_y, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    # todo change keycodes
    def move_up_right(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_U, tcod.event.K_u, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    # todo change keycodes
    def move_down_left(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_B, tcod.event.K_b, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    # todo change keycodes
    def move_down_right(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_N, tcod.event.K_n, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    def pickup(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_G, tcod.event.K_g, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    def inventory(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_I, tcod.event.K_i, tcod.event.Modifier.NONE))
        self.render_console()

        return self.root_console.__str__()

    def descend(self):

        self.handle_event(tcod.event.KeyDown(tcod.event.SCANCODE_PERIOD, tcod.event.K_PERIOD, tcod.event.Modifier.SHIFT))
        self.render_console()

        return self.root_console.__str__()

    def inventory_key(self, key):
        offset = ord("a") - ord(key)
        scancode = tcod.event.SCANCODE_A + offset
        sym = tcod.event.K_a + offset

        self.handle_event(tcod.event.KeyDown(scancode, sym, tcod.event.Modifier.NONE))
        self.render_console()

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


def start_instance(pipe):
    '''s = zerorpc.Server(Main())
    s.bind("tcp://0.0.0.0:4242")
    s.run()'''

    c = Main()
    while True:
        console = pipe.recv()
        if console == "quit":
            return
        elif console == "up":
            pipe.send(c.move_up())
        elif console == "down":
            pipe.send(c.move_down())
        elif console == "left":
            pipe.send(c.move_left())
        elif console == "right":
            pipe.send(c.move_right())
        elif console == "up left":
            pipe.send(c.move_up_left())
        elif console == "up right":
            pipe.send(c.move_up_right())
        elif console == "down left":
            pipe.send(c.move_down_left())
        elif console == "down right":
            pipe.send(c.move_down_right())
        elif console == "pickup":
            pipe.send(c.pickup())
        elif console == "descend":
            pipe.send(c.descend())
        elif console == "inventory":
            pipe.send(c.inventory())
            console = str(input())
            while True:
                if len(console) < 1 and ord("a") <= ord(console) <= ord("z"):
                    pipe.send(c.inventory_key(console))
                    break
                else:
                    pipe.send("input only one lowercase letter")
        else:
            pipe.send("invalid input")


if __name__ == "__main__":
    start_instance()

