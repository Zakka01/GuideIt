from Parsing import parsing_config


def main() -> None:
    config = parsing_config()
    for key, value in config.items():
        print(f"{key.upper()} : {value}")


if __name__ == "__main__":
    main()
