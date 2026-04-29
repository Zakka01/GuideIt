from zone import Zone
from typing import List
from connection import Connection


class Drone:

    def __init__(self, id: str, path: List[Zone]):
        self.id = id
        self.path = path
        self.status = "waiting"
        self.current_pos = 0

    def current_zone(self) -> Zone:
        return self.path[self.current_pos]

    def next_zone(self) -> Zone:
        return self.path[self.current_pos + 1]

    def deliver(self):
        self.status = "delivered"

    def move(self):
        self.current_pos += 1
        self.status = "moving"

    def is_delivered(self) -> bool:
        return self.current_pos >= len(self.path) - 1

    def can_move(self) -> int:
        if self.current_pos >= len(self.path) - 1:
            return False

        next_zone = self.next_zone()
        return next_zone.is_empty()

    def on_connection(self):
        return isinstance(self, Connection)

    def on_zone(self):
        return isinstance(self, Zone)
