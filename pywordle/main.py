import argparse

from gui.main import main as gui_main
from cli import main as cli_main

def main(cli_mode: bool = False):
    if cli_mode:
        cli_main()
    else:
        gui_main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cli", action="store_true")
    args = parser.parse_args()
    
    main(args.cli)

