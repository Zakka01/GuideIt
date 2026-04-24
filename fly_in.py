from parsing import parsing_config
from graph import Graph
from drone import Drone
from typing import List
from simulator import Simulator


def get_drones_nb(config) -> int:
    return config["nb_drones"]


def assign_path_to_drone(nb_drones: int, all_paths: List) -> List:
    drones = []
    for i in range(nb_drones):
        path = all_paths[i % len(all_paths)]["path"]
        drone = Drone(f"D{i+1}", path)
        drones.append(drone)
    return drones


def main() -> None:
    config = parsing_config()

    nb_drones = get_drones_nb(config)
    graph = Graph(config)

    all_paths = graph.find_all_paths()
    all_paths = sorted(all_paths, key=lambda path: path["cost"])

    drones = assign_path_to_drone(nb_drones, all_paths)

    simulator = Simulator(drones, graph.start_hub, graph.end_hub)
    simulator.play()


if __name__ == "__main__":
    main()
