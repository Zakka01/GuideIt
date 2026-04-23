from Parsing import parsing_config
from Flyin.Fly_in import Path_finder


def main() -> None:
    config = parsing_config()

    path_finder = Path_finder(config)
    path_finder.find_shortest_path()


if __name__ == "__main__":
    main()
