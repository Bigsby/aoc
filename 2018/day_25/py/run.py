#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Point = Tuple[int,int,int,int]


def part1(points: List[Point]):
    edges = [ set() for _ in range(len(points)) ]
    for thisPoint, (w0, x0, y0, z0) in enumerate(points):
        for thatPoint, (w1, x1, y1, z1) in enumerate(points):
            if abs(w0 - w1) + abs(x0 - x1) + abs(y0 - y1) + abs(z0 - z1) < 4:
                edges[thisPoint].add(thatPoint)

    visited = set()
    constellations = 0
    for thisPoint in range(len(points)):
        if thisPoint in visited:
            continue
        constellations += 1
        queue = [ thisPoint ]
        while queue:
            currentPoint = queue.pop(0)
            if currentPoint in visited:
                continue
            visited.add(currentPoint)
            for other in edges[currentPoint]:
                queue.append(other)
    return constellations


def part2(puzzleInput):
    pass


def getInput(filePath: str) -> List[Point]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        points = []
        for line in file.readlines():
            points.append(tuple(map(int,line.strip().split(","))))
        return points


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