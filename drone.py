from zone import Zone
from typing import List
from connection import Connection


class Drone:

    def __init__(self, id: str, path: List[Zone]):
        self.id = id
        self.path = path
        self.current_pos = 0

    def current_zone(self) -> Zone:
        return self.path[self.current_pos]

    def next_zone(self) -> Zone:
        return self.path[self.current_pos + 1]

    def next_of_next_zone(self) -> Zone:
        return self.path[self.current_pos + 2]

    def deliver(self):
        self.status = "delivered"

    def move(self):
        self.current_pos += 1
        self.status = "moving"

    def is_delivered(self) -> bool:
        return self.current_pos >= len(self.path) - 1

    def can_move(self) -> int:
        next_index = self.current_pos + 1

        if next_index >= len(self.path):
            return False

        next_zone = self.path[next_index]

        if not next_zone.has_space():
            return False

        return True

    def on_connection(self, current_zone):
        return isinstance(current_zone, Connection)

    def on_zone(self, current_zone):
        return isinstance(current_zone, Zone)
