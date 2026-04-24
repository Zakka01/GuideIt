from zone import Zone
from typing import List
from connection import Connection
from collections import deque


class Graph:

    def __init__(self, config: dict):
        self.config = config
        self.start_hub = Zone(config["start_hub"])
        self.end_hub = Zone(config["end_hub"])
        self.connection_dict = self.zone_neighbors()
        self.paths = []

    def zone_neighbors(self) -> dict:
        config = self.config
        zones: List = []
        zones_lookup: dict = {}
        connection_dict: dict = {}

        for key, value in config.items():
            if key in ["start_hub", "end_hub"]:
                zone = Zone(config[key])
                zones.append(zone)
            elif key == "hub":
                for value in config[key]:
                    zone = Zone(value)
                    zones.append(zone)

        for zone in zones:
            zones_lookup[zone.name] = zone

        connection = config["connection"]
        for c in connection:
            from_dst = c["from"]
            to_dst = c["to"]
            capacity = c["max_link_capacity"]

            if from_dst not in connection_dict:
                connection_dict[from_dst] = []
            if to_dst not in connection_dict:
                connection_dict[to_dst] = []

            connection_dict[from_dst].append((zones_lookup[to_dst], capacity))

        return connection_dict

    def build_paths(self, path: List):
        cost = 0
        for p in path[1:]:
            if not isinstance(p, Connection):
                cost += p.it_cost()

        self.paths.append({
            "path": path,
            "cost": cost
        })

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

                if neighbor.is_zone_resticted():
                    connection = Connection(current_zone, neighbor, capacity)
                    new_path = path_so_far + [connection] + [neighbor]
                    queue.append((neighbor, new_path))

                else:
                    if neighbor.is_zone_priority():
                        queue.appendleft((neighbor, path_so_far + [neighbor]))
                    else:
                        queue.append((neighbor, path_so_far + [neighbor]))

        return self.paths
