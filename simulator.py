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
            turns = 0

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

            valid_moves = []
            for move in drones_moves:
                valid_moves.append(move)

            for move in valid_moves:
                print(f"{move['drone'].id} - {move['dst'].name}")
                move["drone"].move()
                move["dst"].drone_in += 1

            turns += 1

            if all(drone.is_delivered() for drone in self.drones):
                break
