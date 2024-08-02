from connector.cli import run_command

from {name}.async_.lumos import AsyncCommands
from {name}.sync_.lumos import SyncCommands


def main():
    run_command(SyncCommands(), AsyncCommands())


if __name__ == "__main__":
    main()
