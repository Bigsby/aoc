import sys, os

directions = {
    "^": (0, -1),
    "v": (0, 1),
    ">": (1, 0),
    "<": (-1,0)
    }

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath) as file:
        for c in file.read():
            if c in directions:
                yield directions[c]
