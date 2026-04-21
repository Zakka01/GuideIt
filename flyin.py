from Parsing import parsing_config
from Path_finder.hub import Hub
from typing import List


def get_hubs_stats(config) -> dict:

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

    for key, value in connection_dict.items():
        for val in value:
            print(f"{key}: {val.name}")


def main() -> None:
    config = parsing_config()
    get_hubs_stats(config)
    for key, value in config.items():
        if key in ["hub", "connection"]:
            print()
            print(key.upper())
            for v in value:
                print(v)
        else:
            print()
            print(f"{key.upper()}")
            print(f"{value}")


if __name__ == "__main__":
    main()
