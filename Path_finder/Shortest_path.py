from collections import deque
from typing import List
from Path_finder.hub import Hub
from Parsing import parsing_config


class Path_finder:

    def __init__(self, config: dict):
        self.config = config
        self.start_hub = Hub(config["start_hub"])
        self.end_hub = Hub(config["end_hub"])
        self.connection_dict = self.hubs_neighbors()

    def hubs_neighbors(self) -> dict:
        config = self.config
        hubs: List = []
        hubs_lookup: dict = {}
        connection_dict: dict = {}

        for key, value in config.items():
            if key in ["start_hub", "end_hub"]:
                hub = Hub(config[key])
                hubs.append(hub)
            elif key == "hub":
                for value in config[key]:
                    hub = Hub(value)
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

    def find_shortest_path(self) -> list:

        hubs = deque([self.start_hub])
        visited = set()
        path = {self.start_hub: None}
        visited.add(self.start_hub)
        cost = 0

        while hubs:
            current_hub = hubs.popleft()
            neighbors = self.connection_dict[current_hub.name]

            if not neighbors:
                hubs.pop()
                continue

            for neighbor in neighbors:
                cost = neighbor.it_cost()
                if 
