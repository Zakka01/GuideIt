from drone import Drone
from zone import Zone
from connection import Connection
from typing import List
from collections import defaultdict


class Simulator:

    def __init__(self, drones: List[Drone],
                 start_hub: Zone,
                 end_hub: Zone,
                 all_zones: List[Zone],
                 connection_dict: dict):

        self.all_zones = all_zones
        self.drones = drones
        self.start = start_hub
        self.end = end_hub
        self.connections = connection_dict
        self.output = []
        self.turns = 0

    def is_all_delivered(self) -> bool:
        return all(drone.is_delivered() for drone in self.drones)

    def will_be_free_next_turn(self, restricted: Zone) -> bool:

        current_capacity = restricted.drone_in

        if current_capacity == 0:
            return True

        if current_capacity >= restricted.max_drones:
            return False

        return True

    def validate_moves(self, drones_moves: List):
        valid_moves = []
        dst_count = defaultdict(int)

        drones_moves.sort(key=lambda m: int(m["drone"].id[1:]))

        for move in drones_moves:
            dst = move["dst"]
            dst_name = dst.name

            if isinstance(dst, Connection):
                max_capacity = dst.capacity
            else:
                max_capacity = dst.max_drones

            if dst_count[dst_name] < max_capacity:
                valid_moves.append(move)
                dst_count[dst_name] += 1

        return valid_moves

    def apply_moves(self, valid_moves: List):
        for move in valid_moves:
            drone = move["drone"]
            dst = move["dst"]
            move_type = move["type"]

            if move_type == "normal_move":
                drone.move()
                dst.drone_in += 1

            elif move_type == "connection_enter":
                drone.move()
                dst.drone_in += 1
                drone.on_connection = True

            elif move_type == "connection_exit":
                drone.move()
                dst.drone_in += 1
                drone.on_connection = False

    def record_turn_output(self, valid_moves: List[dict]):

        if not valid_moves:
            return

        turn_output = []
        for move in valid_moves:
            drone_id = move["drone"].id
            destination_name = move["dst"].name
            turn_output.append(f"{drone_id}-{destination_name}")

        output_line = " ".join(turn_output)
        self.output.append(output_line)
        print(output_line)

    def reset_zone_capacity(self):
        for zone in self.all_zones:
            zone.drone_in = 0

    def get_connection(self, current: Zone, next: Zone) -> dict:
        from_dst = current
        to_dst = None

        neighbors_of_current = self.connections[current.name]
        for neighbor in neighbors_of_current:
            if neighbor[0] == next:
                to_dst = neighbor[0]
                connection_capacity = neighbor[1]

        return {
            "from": from_dst,
            "to": to_dst,
            "connection_capacity": connection_capacity
        }

    # def update_zone_occupancy(self):
    #     for drone in self.drones:
    #         if not drone.is_delivered():
    #             current = drone.current_zone()
    #             current.drone_in += 1

    def play(self) -> int:

        while not self.is_all_delivered():
            drones_moves = []

            for drone in self.drones:
                if drone.is_delivered():
                    continue

                if drone.on_connection():
                    connection = drone.current_zone()
                    drones_moves.append({
                        "drone": drone,
                        "dst": connection.to_dst,
                        "type": "connection_exit"
                    })

                elif drone.can_move():
                    next_zone = drone.next_zone()
                    current_zone = drone.current_zone()
                    print(f">>>> {current_zone.name} {current_zone.drone_in}")
                    print(f">>>> {next_zone.name} {next_zone.drone_in}")

                    connection = self.get_connection(current_zone, next_zone)
                    capacity = connection["connection_capacity"]

                    if next_zone.is_zone_restricted():
                        if self.will_be_free_next_turn(next_zone):
                            drones_moves.append({
                                "drone": drone,
                                "dst": drone.current_zone(),
                                "type": "connection_enter",
                                "connection_capacity": capacity,
                                "target": next_zone
                            })
                    else:
                        drones_moves.append({
                            "drone": drone,
                            "dst": next_zone,
                            "connection_capacity": capacity,
                            "type": "normal_move",
                        })

            valid_moves = self.validate_moves(drones_moves)
            self.apply_moves(valid_moves)
            self.record_turn_output(valid_moves)

            self.reset_zone_capacity()

            self.turns += 1

        return self.turns
