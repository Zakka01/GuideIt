from zone import Zone
from typing import List
from connection import Connection


class Drone:

    def __init__(self, id: str, path: List[Zone]):
        self.id = id
        self.path = path
        self.status = "waiting"
        self.current_pos = 0
        self.on_connection_area = False

    def current_zone(self) -> Zone:
        return self.path[self.current_pos]

    def next_zone(self) -> Zone:
        return self.path[self.current_pos + 1]

    def deliver(self):
        self.status = "delivered"

    def move(self):
        self.current_pos += 1

    def is_delivered(self) -> bool:
        return self.path[self.current_pos] == self.path[-1]

    def can_move(self):
        if self.current_pos >= len(self.path) - 1:
            return False

        next_zone = self.next_zone()

        if isinstance(next_zone, Connection):
            next_zone.current_capacity += 1
            return next_zone.has_capacity()

        elif isinstance(next_zone, Zone):
            return next_zone.get_max_drones()
