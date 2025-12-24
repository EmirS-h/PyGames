import os
import sys

# Optional: Ensure the current directory is explicitly in path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from games.space_shooters.main import SpaceShooter


def main():
    game = SpaceShooter()
    game.run()


if __name__ == "__main__":
    main()
