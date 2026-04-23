from collections import deque
from typing import List


class Zone:

    def __init__(self, config: dict) -> None:
        self.name = config["name"]
        self.y = config["y"]
        self.x = config["x"]
        self.zone_type = config["zone"]
        self.color = config["color"]
        self.max_drones = config["max_drones"]
        self.is_path = False

    def is_zone_blocked(self) -> bool:
        return self.zone_type == "blocked"

    def is_zone_resticted(self) -> bool:
        return self.zone_type == "restricted"

    def is_zone_normal(self) -> bool:
        return self.zone_type == "normal"

    def is_zone_priority(self) -> bool:
        return self.zone_type == "priority"

    def it_cost(self) -> int:
        if self.is_zone_resticted:
            return 2
        return 1

    def get_max_drones(self) -> int:
        return self.max_drones


class Path_finder:

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
            # connection_dict[to_dst].append((zones_lookup[from_dst], capacity))

        return connection_dict

    def build_path(self, parent: dict, end_hub: Zone):
        key_hub = end_hub

        while key_hub:
            self.paths.append(key_hub)
            key_hub = parent.get(key_hub)

        self.paths.reverse()
        for p in self.paths:
            p.is_path = True

        for p in self.paths:
            print(p.name)

    def find_shortest_path(self) -> None:

        zones = deque([self.start_hub])
        visited = set()
        parent = {self.start_hub: None}
        visited.add(self.start_hub)

        while zones:
            current_hub = zones.popleft()

            # stop when we reach the end , and we reconstruct the path
            if current_hub.name == self.end_hub.name:
                self.build_path(parent, current_hub)
                return

            neighbors = self.connection_dict[current_hub.name]
            for neighbor, capacity in neighbors:
                if neighbor in visited:
                    continue

                if neighbor.is_zone_blocked():
                    continue

                if neighbor.is_zone_priority():
                    visited.add(neighbor)
                    parent[neighbor] = current_hub
                    zones.append(neighbor)
                    break

                visited.add(neighbor)
                parent[neighbor] = current_hub
                zones.append(neighbor)
