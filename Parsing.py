import sys


def parse_connection(value: str) -> dict:

    max_link_capacity = 1

    if "[" in value:
        dist, metadata = value.strip().split(" ", 1)
        metadata = metadata.strip()

        if not (metadata.startswith("[") and metadata.endswith("]")):
            raise ValueError("Invalid metadata")

        metadata = metadata.strip("[]")
        if "=" not in metadata:
            raise ValueError("Invalid metadata")

        key, value = metadata.split("=", 1)
        if key != "max_link_capacity":
            raise ValueError("Invalid Metadata for connection")

        max_link_capacity = int(value)
    else:
        dist = value

    if "-" not in dist:
        raise ValueError("Invalid connection format")
    from_dist, to_dist = dist.strip().split("-", 1)

    return {
        "from": from_dist,
        "to": to_dist,
        "max_link_capacity": max_link_capacity
    }


def parse_hub(value: str) -> dict:
    name, x, other = value.strip().split(" ", 2)

    metadata_dict = {}
    y = 0

    if " " in other:

        y, metadata = other.split(" ", 1)

        if not metadata.startswith("[") or not metadata.endswith("]"):
            raise ValueError("Invalid Metadata")

        if "=" not in metadata:
            raise ValueError("Invalid Metadata")

        metadata = metadata.strip("[]")
        pairs = metadata.split()
        for pair in pairs:
            if "=" not in pair:
                raise ValueError("Invalid Metadata format")
            key, value = pair.split("=", 1)
            if key not in ["zone", "color", "max_drones"]:
                raise ValueError("Invalid Metadata Key")

            metadata_dict[key] = value

    else:
        y = other

    return {
        "name": name,
        "x": int(x),
        "y": int(y),
        "color": metadata_dict["color"],

        "zone": metadata_dict["zone"]
        if "zone" in metadata_dict else "normal",

        "max_drones": int(metadata_dict["max_drones"])
        if "max_drones" in metadata_dict else 1
    }


def validate_config(config: dict) -> dict:
    try:

        parsed_config = {}
        for key, value in config.items():
            if key == "nb_drones":
                parsed_config[key] = int(value)

            elif key in ["start_hub", "end_hub"]:
                parsed_config[key] = parse_hub(value)

            elif key == "hub":
                for v in value:
                    parsed_config["hub"] = [parse_hub(v) for v in value]

            elif key == "connection":
                if key not in parsed_config:
                    parsed_config[key] = []
                for v in value:
                    connection_value = parse_connection(v)
                    parsed_config[key].append(connection_value)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(0)

    return parsed_config


def validate_connection_hubs(config: dict) -> None:

    start_hub = config["start_hub"]["name"]
    end_hub = config["end_hub"]["name"]
    hubs = config["hub"]
    connection = config["connection"]

    all_hubs = set()
    for hub in hubs:
        all_hubs.add(hub["name"])
    all_hubs.add(start_hub)
    all_hubs.add(end_hub)

    for c in connection:
        from_dist, to_dist = c["from"], c["to"]
        if from_dist not in all_hubs:
            raise ValueError(f"Unknown hub: {from_dist}")

        if to_dist not in all_hubs:
            raise ValueError(f"Unknown hub: {to_dist}")


def parsing_config() -> dict:

    try:
        config: dict = {}
        mandatory_keys = [
            "nb_drones",
            "start_hub",
            "end_hub"
        ]
        extra_keys = [
            "hub",
            "connection"
        ]

        if len(sys.argv) == 2:
            filename = sys.argv[1]
            with open(filename, "r") as file:
                for line in file:
                    line = line.strip()

                    if line.startswith("#"):
                        continue

                    elif line == "":
                        continue

                    elif ":" not in line:
                        raise ValueError("Invalid config line")

                    else:
                        key, value = line.split(":", 1)
                        key, value = key.lower().strip(), value.strip()
                        if not value:
                            raise ValueError(f"No value given for {key}")

                        if key in mandatory_keys and key in config:
                            raise ValueError("Duplicate Lines")

                        if key not in mandatory_keys and key not in extra_keys:
                            raise ValueError(f"Key: '{key}' is not Valid")

                        if key in mandatory_keys:
                            config[key] = value

                        elif key in extra_keys:
                            if key not in config:
                                config[key] = []
                            config[key].append(value)

        else:
            raise ValueError("No config file given")

        if (
            "nb_drones" not in config
            or "start_hub" not in config
            or "end_hub" not in config
        ):
            raise ValueError("Missing a mandatory key")

        valid_config = validate_config(config)
        validate_connection_hubs(valid_config)

    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(0)

    return valid_config
