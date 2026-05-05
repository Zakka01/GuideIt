from parsing import Parser
from graph import Graph
from drone import Drone
from typing import List
from simulator import Simulator
from render import Render


class Main:

    def get_drones_nb(self, config) -> int:
        return config["nb_drones"]

    def assign_path_to_drone(self, nb_drones: int, all_paths: List) -> List:
        drones = []

        selected_paths = all_paths[:2] if len(all_paths) >= 2 else all_paths

        for i in range(nb_drones):
            path = selected_paths[i % len(selected_paths)]["path"]
            drone = Drone(f"D{i+1}", path)
            drones.append(drone)
        return drones

    def main(self) -> None:
        parser = Parser()
        config = parser.parsing_config()

        nb_drones = self.get_drones_nb(config)
        graph = Graph(config)

        all_zones = graph.get_all_zones()
        all_paths = graph.find_all_paths()
        all_paths = sorted(all_paths, key=lambda path: path["cost"])
        drones = self.assign_path_to_drone(nb_drones, all_paths)
        connection_dct = graph.build_connection_dict()

        simulator = Simulator(drones,
                              graph.start_hub,
                              graph.end_hub,
                              all_zones,
                              connection_dct)
        simulator.play()

        zones = graph.get_all_zones()
        connections = graph.build_connection_dict()
        render = Render(zones, connections)


if __name__ == "__main__":
    main = Main()
    main.main()
