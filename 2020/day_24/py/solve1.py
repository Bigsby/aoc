#! /usr/bin/python3

from common import getInput, flipInitialTiles, getTotalBlackCount


def main():
    tilePaths = list(getInput())
    tiles = flipInitialTiles(tilePaths)
    result = getTotalBlackCount(tiles)
    print("Black tiles count:", result)


if __name__ == "__main__":
    main()
