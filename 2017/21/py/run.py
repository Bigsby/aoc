#! /usr/bin/python3

import sys
import os
import time
import re
from typing import Dict, Iterable, List, Set, Tuple

Position = complex
Grid = Set[Position]
Rule = Tuple[Grid, Grid]
Rules = Dict[int, List[Rule]]
START = ".#./..#/###"


def printGrid(grid: Grid):
    maxX = int(max(p.real for p in grid))
    maxY = int(max(p.imag for p in grid))
    for y in range(maxY + 1):
        for x in range(maxX + 1):
            print("#" if x + y * 1j in grid else ".", end="")
        print()
    print()


def parseGrid(text: str) -> Tuple[int, Grid]:
    grid = Grid()
    split = text.split("/")
    for y, line in enumerate(split):
        for x, c in enumerate(line):
            if c == "#":
                grid.add(x + y * 1j)
    return len(split[0]), grid


def mirrorHorizontal(grid: Grid, size: int) -> Grid:
    return {position.imag * 1j + size - 1 - position.real for position in grid}


def rotateClockwise(grid: Grid, size: int) -> Grid:
    return {position.real * 1j + size - 1 - position.imag for position in grid}


def generatePermutations(grid: Grid, size: int) -> Iterable[Grid]:
    for _ in range(4):
        yield grid
        yield mirrorHorizontal(grid, size)
        grid = rotateClockwise(grid, size)


def enhanceGrid(grid: Grid, size: int, rules: List[Rule]) -> Grid:
    for permutation in generatePermutations(grid, size):
        for match, result in rules:
            if match == permutation:
                return result
    raise Exception("Rule not found")


def splitGrid(grid: Grid, count: int, size: int) -> Iterable[Tuple[int, int, Grid]]:
    for yIndex in range(count):
        for xIndex in range(count):
            xOffset = xIndex * size
            yOffset = yIndex * size
            innerGrid = {
                p - (xIndex * size) - (yIndex * size) * 1j
                for p in grid
                if xOffset <= p.real < xOffset + size and yOffset <= p.imag < yOffset + size}
            yield xIndex, yIndex, innerGrid


def iterate(grid: Grid, size: int, rules: Rules) -> Tuple[int, Grid]:
    enhancedGrid = Grid()
    divider = 0
    ruleSize = 0
    if size % 2 == 0:
        ruleSize = 2
    elif size % 3 == 0:
        ruleSize = 3
    ruleSet = rules[ruleSize]
    divider = size // ruleSize
    for xIndex, yIndex, innerGrid in splitGrid(grid, divider, ruleSize):
        for position in enhanceGrid(innerGrid, ruleSize, ruleSet):
            enhancedGrid.add(position + xIndex * (ruleSize +
                                                  1) + yIndex * 1j * (ruleSize + 1))
    return size + divider, enhancedGrid


def runIterations(grid: Grid, size: int, rules: Rules, iterations: int) -> Tuple[int, Grid]:
    for _ in range(iterations):
        size, grid = iterate(grid, size, rules)
    return size, grid


def runNext3Iterations(grid: Grid, rules: Rules) -> List[Grid]:
    _, grid = runIterations(grid, 3, rules, 3)
    return [innerGrid for _, _, innerGrid in splitGrid(grid, 3, 3)]


def getGridId(grid: Grid) -> int:
    result = 0
    for y in range(3):
        for x in range(3):
            if x + y * 1j in grid:
                result += (1 << x) << 3 * y
    return result


def part2(rules: Rules, grid: Grid) -> int:
    total = 0
    calculated: Dict[int, List[Grid]] = {}
    queue: List[Tuple[Grid, int]] = [(grid, 0)]
    while queue:
        grid, iterations = queue.pop()
        if iterations == 18:
            total += len(grid)
        else:
            gridId = getGridId(grid)
            if gridId not in calculated:
                calculated[gridId] = runNext3Iterations(grid, rules)
            for innerGrid in calculated[gridId]:
                queue.append((innerGrid, iterations + 3))
    return total


def solve(rules: Rules) -> Tuple[int, int]:
    size, grid = parseGrid(START)
    return (
        len(runIterations(grid, size, rules, 5)[1]),
        part2(rules, grid)
    )


lineRegex = re.compile(r"^(?P<rule>[./#]+) => (?P<result>[./#]+)$")


def parseLine(line: str) -> Tuple[int, Rule]:
    match = lineRegex.match(line)
    if match:
        ruleSize, ruleGrid = parseGrid(match.group("rule"))
        _, resultGrid = parseGrid(match.group("result"))
        return ruleSize, (ruleGrid, resultGrid)
    raise Exception("Bad format", line)


def getInput(filePath: str) -> Dict[int, List[Rule]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        rules: Dict[int, List[Rule]] = {2: [], 3: []}
        for line in file.readlines():
            size, rule = parseLine(line)
            rules[size].append(rule)
        return rules


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
