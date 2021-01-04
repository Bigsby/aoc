#! /usr/bin/python3

import sys, os, time


NEIGHBOR_DIRECTIONS = [
     - 1 - 1j,
         - 1j,
     + 1 - 1j,
     - 1,
     + 1,
     - 1 + 1j,
         + 1j,
     + 1 + 1j
]
def getNeighbors(pos):
    for direction in NEIGHBOR_DIRECTIONS:
        yield pos + direction


def getNextState(grid, alwaysOn = []):
    for position in alwaysOn:
            grid[position] = 1
    newState = dict(grid)
    for position in grid:
        neighbors = sum(map(lambda neighbor: grid[neighbor] if neighbor in grid else 0, getNeighbors(position)))
        if grid[position]:
            newState[position] = 1 if neighbors == 2 or neighbors == 3 else 0
        else:
            newState[position] = 1 if neighbors == 3 else 0
    for position in alwaysOn:
            newState[position] = 1
    return newState


def runSteps(grid, alwaysOn = []):
    for _ in range(100):
        grid = getNextState(grid, alwaysOn)
    return sum(grid.values())


def part1(grid):
    return runSteps(grid)


def part2(grid):
    side = max(map(lambda key: key.real, grid.keys()))
    alwaysOn = [
        0,
        side * 1j,
        side,
        side * (1 + 1j)
    ]
    return runSteps(grid, alwaysOn)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        grid = {}
        pos = 0j
        for line in file.readlines():
            for c in line.strip():
                grid[pos] = 1 if c == "#" else 0
                pos += 1
            pos += 1j - pos.real
        return grid


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()