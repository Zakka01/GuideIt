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

        while True:
            drones_moves = []

            for drone in self.drones:
                if drone.is_delivered():
                    continue

                if drone.on_connection():
                    connection = drone.current_zone()
                    drones_moves.append({
                        "drone": drone,
                        "dst": connection.to_dst
                    })

                if drone.can_move():
                    next_zone = drone.next_zone()
                    drones_moves.append({
                        "drone": drone,
                        "dst": next_zone
                    })

                drone.move()
                next_zone.drone_in += 1
