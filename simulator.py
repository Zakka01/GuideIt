from drone import Drone
from zone import Zone
# from connection import Connection
from typing import List


class Simulator:

    def __init__(self, drones: List[Drone], start_hub: Zone, end_hub: Zone):
        self.drones = drones
        self.start = start_hub
        self.end = end_hub

    def is_all_delivered(self) -> bool:
        for drone in self.drones:
            if drone.path[-1] != self.end:
                return False
        return True

    def play(self):
        for drone in self.drones:
            if not drone.is_delivered():

                if drone.on_connection():
                    drone.move()

                if drone.can_move():
                    next_zone_in_path = drone.next_zone()
                    
