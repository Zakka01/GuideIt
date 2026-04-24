from drone import Drone
from zone import Zone
# from connection import Connection
from typing import List


class Simulator:

    def __init__(self, drones: List[Drone], start_hub: Zone, end_hub: Zone):
        self.drones = drones
        self.start = start_hub
        self.end = end_hub

    def play(self):
        ...
