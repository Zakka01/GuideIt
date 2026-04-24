from parsing import parsing_config
from path_finder import PathFinder


def main() -> None:
    config = parsing_config()

    path_finder = PathFinder(config)
    path_finder.find_all_paths()


if __name__ == "__main__":
    main()
