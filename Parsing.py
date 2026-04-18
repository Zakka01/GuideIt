import sys

def parsing_config() -> dict:
    """
        Parse the Config File, Validate and Store the Data
        in a Dict, Handle the Error using try/Except to prevent
        Crashes
    """


    # Get Line, Strip it, Split based on ':', Store key value
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
                            key, val = line.strip(":", 1)
                            key, val = key.lower().strip(), val.strip()
                            if not val:
                                raise ValueError(f"No value given for {key}")
                            if key in mandatory_keys and key in config:
                                raise ValueError("Duplicate Lines")
                            if key not in mandatory_keys and key not in extra_keys:
                                raise ValueError(f"Key: '{key}' is not Valid")

                            config[key] = val      
        else:
            raise ValueError("No config file given")
        
        missing_keys = set(mandatory_keys) - set(config.keys())
        if missing_keys:
            raise ValueError(f"Missing keys: {missing_keys}")
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(0)

    return config