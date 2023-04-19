from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from tcod.console import Console
from tcod.map import compute_fov

import exceptions
from message_log import MessageLog
import render_functions

if TYPE_CHECKING:
    from entity import Actor
    from game_map import GameMap, GameWorld


class Engine:
    game_map: GameMap
    game_world: GameWorld

    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player
        self.point_counter = 0
        self.num_explored = 0
        self.num_turns = 0
        self.total_points = 0

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass  # Ignore impossible action exceptions from AI.

    def update_fov(self) -> None:
        """Recompute the visible area based on the players point of view."""
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )
        # If a tile is "visible" it should be added to "explored".
        self.game_map.explored |= self.game_map.visible
        self.num_explored = np.count_nonzero(self.game_map.explored)

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_functions.render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_functions.render_dungeon_level(
            console=console,
            dungeon_level=self.game_world.current_floor,
            location=(0, 47),
        )

        render_functions.render_points(
            console=console,
            points=self.get_points(),
            location=(0, 49)
        )
        render_functions.render_names_at_mouse_location(
            console=console, x=21, y=44, engine=self
        )

    def turns_taken(self):
        self.num_turns += 1

    def award_points(self, points: int) -> None:
        self.point_counter += points

    def get_points(self) -> int:
        return self.point_counter + self.num_explored

    def get_total_points(self) -> int:
        return self.total_points

    def total_points_in_level(self) ->None:
        turn_bonus = 500 - self.num_turns
        if turn_bonus > 0:
            self.total_points = self.get_points() + turn_bonus
            self.message_log.add_message(f"Level completed in {self.num_turns} turns. You earned {turn_bonus} bonus points!")
        else:
            self.total_points = self.get_points()
            self.message_log.add_message(f"Level completed in {self.num_turns} turns. Complete the level in less "
                                         f"turns for bonus points!")
        self.point_counter = 0

