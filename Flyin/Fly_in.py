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


class Path_finder:

    def __init__(self, config: dict):
        self.config = config
        self.start_hub = Zone(config["start_hub"])
        self.end_hub = Zone(config["end_hub"])
        self.connection_dict = self.hubs_neighbors()
        self.paths = []

    def hubs_neighbors(self) -> dict:
        config = self.config
        hubs: List = []
        hubs_lookup: dict = {}
        connection_dict: dict = {}

        for key, value in config.items():
            if key in ["start_hub", "end_hub"]:
                hub = Zone(config[key])
                hubs.append(hub)
            elif key == "hub":
                for value in config[key]:
                    hub = Zone(value)
                    hubs.append(hub)

        for hub in hubs:
            hubs_lookup[hub.name] = hub

        connection = config["connection"]
        for c in connection:
            from_dst = c["from"]
            to_dst = c["to"]

            if from_dst not in connection_dict:
                connection_dict[from_dst] = []
            if to_dst not in connection_dict:
                connection_dict[to_dst] = []

            connection_dict[from_dst].append(hubs_lookup[to_dst])
            connection_dict[to_dst].append(hubs_lookup[from_dst])

        return connection_dict

    def build_path(self, parent: dict, end_hub: Zone):
        key_hub = self.end_hub

        while key_hub:
            self.paths.append(key_hub)
            key_hub = parent.get(key_hub)
        self.paths.reverse()

        for p in self.paths:
            p.is_path = True

    def find_shortest_path(self) -> list:

        hubs = deque([self.start_hub])
        visited = set()
        parent = {self.start_hub: None}
        visited.add(self.start_hub)

        while hubs:
            current_hub = hubs.popleft()

            # stop when we reach the end , and we reconstruct the path
            if current_hub == self.end_hub:
                break

            for neighbor in self.connection_dict[current_hub.name]:
                if neighbor in visited:
                    continue

                if neighbor.is_zone_blocked():
                    continue

                visited.add(neighbor)
                parent[neighbor] = current_hub
                hubs.append(neighbor)

        self.build_path(parent, self.end_hub)
