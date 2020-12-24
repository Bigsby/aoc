import sys, os, re

lineRegex = re.compile(r"e|se|sw|w|nw|ne")

steps = {
    "e": (1,-1,0),
    "se": (0,-1,1),
    "sw": (-1,0,1),
    "w": (-1,1,0),
    "nw": (0,1,-1),
    "ne": (1,0,-1)
}


def flipInitialTiles(tilePaths):
    tiles = {}
    for path in tilePaths:
        current = (0,0,0)
        for direction in path:
            step = steps[direction]
            current = current[0] + step[0], current[1] + step[1], current[2] + step[2]
        if current in tiles:
            tiles[current] = not tiles[current]
        else:
            tiles[current] = True
    return tiles


def getTotalBlackCount(tiles):
    return sum([tiles[position] for position in tiles if tiles[position] ])


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            yield lineRegex.findall(line.strip())
