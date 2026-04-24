from zone import Zone
from typing import List


class Drone:

    def __init__(self, id: str, path: List[Zone]):
        self.id = id
        self.path = []
        self.status = "waiting"
        self.current_pos = 0
        self.turns = 0

    def which_zone(self):
        return self.path[self.current_pos]
