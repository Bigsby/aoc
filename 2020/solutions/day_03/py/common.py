import sys, os
from typing import List, Tuple


def getInput() -> List[List[int]]:
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)


    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)
    
    grid = []

    try:
        with open(filePath) as inputFile:
            for line in inputFile.readlines():
                row = []
                for c in line:
                    if c == '#':
                        row.append(1)
                    elif c == '.':
                        row.append(0)
                    elif c == '\n':
                        break 
                    else:
                        raise Exception("Unrecognized character in input", str(ord(c)))
                grid.append(row)

 
    except Exception as ex:
        print("Error reading file")
        print(ex.args[0])
        sys.exit(1)

    return grid  


def getNextPosition(currentPosition: Tuple[int,int], step: Tuple[int,int]) -> Tuple[int,int]:
    return (currentPosition[0] + step[0], currentPosition[1] + step[1])


def calculateTrees(grid: List[List[int]], step: Tuple[int,int]) -> int:
    lastRow = len(grid)
    lastColumn = len(grid[0])
    currentPosition = (0, 0)
    treeCount = 0
    while currentPosition[0] < lastRow:
        treeCount = treeCount + grid[currentPosition[0]][currentPosition[1] % lastColumn]
        currentPosition = getNextPosition(currentPosition, step)
    return treeCount


