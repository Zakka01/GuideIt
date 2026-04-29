from zone import Zone
from typing import List
from connection import Connection
from collections import deque


class Graph:

    def __init__(self, config: dict):
        self.config = config
        self.all_zones = self.get_all_zones()
        self.zone_lookup = {z.name: z for z in self.all_zones}
        self.start_hub = self.zone_lookup[config["start_hub"]["name"]]
        self.end_hub = self.zone_lookup[config["end_hub"]["name"]]
        self.connection_dict = self.build_connection_dict()
        self.paths = []

    def get_all_zones(self) -> List[Zone]:

        all_zones = []

        if "start_hub" in self.config:
            all_zones.append(Zone(self.config["start_hub"]))

        if "end_hub" in self.config:
            all_zones.append(Zone(self.config["end_hub"]))

        if "hub" in self.config:
            for hub_data in self.config["hub"]:
                all_zones.append(Zone(hub_data))

        return all_zones

    def build_connection_dict(self) -> dict:

        connection_dict = {}
        for zone in self.all_zones:
            connection_dict[zone.name] = []

        for c in self.config["connection"]:
            from_name = c["from"]
            to_name = c["to"]
            capacity = c.get("max_link_capacity", 1)

            from_zone = self.zone_lookup[from_name]
            to_zone = self.zone_lookup[to_name]

            connection_dict[from_name].append((to_zone, capacity))
            connection_dict[to_name].append((from_zone, capacity))
        return connection_dict

    def build_paths(self, path: List):
        cost = 0
        for p in path[1:]:
            if not isinstance(p, Connection):
                cost += p.it_cost()

        self.paths.append({"path": path, "cost": cost})

    def find_all_paths(self) -> List[dict]:

        queue = deque([(self.start_hub, [self.start_hub])])

        while queue:
            current_zone, path_so_far = queue.popleft()

            # stop when we reach the end, and we build the path
            if current_zone.name == self.end_hub.name:
                self.build_paths(path_so_far)
                continue

            neighbors = self.connection_dict[current_zone.name]
            for neighbor, capacity in neighbors:
                if neighbor in path_so_far:
                    continue

                if neighbor.is_zone_blocked():
                    continue

                if neighbor.is_zone_restricted():
                    connection = Connection(current_zone, neighbor, capacity)
                    new_path = path_so_far + [connection] + [neighbor]
                    queue.append((neighbor, new_path))

                else:
                    if neighbor.is_zone_priority():
                        queue.appendleft((neighbor, path_so_far + [neighbor]))
                    else:
                        queue.append((neighbor, path_so_far + [neighbor]))

        for p in self.paths:
            for key, value in p.items():
                if key == "path":
                    for v in value:
                        if not isinstance(v, Connection):
                            print(f"({v.max_drones}) {v.name}")
                        else:
                            print(f"   @{v.connection_name}")

                else:
                    print("->", value)
            print()

        return self.paths
