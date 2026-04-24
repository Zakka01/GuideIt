from parsing import parsing_config
from graph import Graph


def main() -> None:
    config = parsing_config()

    path_finder = Graph(config)
    path_finder.find_all_paths()


if __name__ == "__main__":
    main()
