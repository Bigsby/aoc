#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re

FileSystem = Dict[complex, Tuple[int, int]]


def getEmptyAndNonViableNodes(fileSystem: FileSystem) -> Tuple[complex, List[complex]]:
    nodeNames = fileSystem.keys()
    empty = -0j
    nonViableNodes = set()
    for thisNode in nodeNames:
        thisUsed = fileSystem[thisNode][1]
        if thisUsed == 0:
            empty = thisNode
            continue
        for otherNode in nodeNames:
            if otherNode == thisNode:
                continue
            if thisUsed > fileSystem[otherNode][0]:
                nonViableNodes.add(thisNode)
    return empty, list(nonViableNodes)


DIRECTIONS = [-1j, -1, 1, 1j]


def getStepsToTarget(nodes: List[complex], nonViable: List[complex], start: complex, destination: complex) -> int:
    visited = [start]
    queue: List[Tuple[complex, int]] = [(start, 0)]
    while queue:
        currentNode, length = queue.pop(0)
        for direction in DIRECTIONS:
            newNode = currentNode + direction
            if newNode == destination:
                return length + 1
            if newNode in nodes and newNode not in visited and newNode not in nonViable:
                visited.append(newNode)
                queue.append((newNode, length + 1))
    raise Exception("Path not found")


def solve(fileSystem: FileSystem) -> Tuple[int, int]:
    empty, nonViable = getEmptyAndNonViableNodes(fileSystem)
    nodes = list(fileSystem.keys())
    emptyDestination = int(max(n.real for n in nodes))
    return (
        len(fileSystem) - len(nonViable) - 1,
        getStepsToTarget(nodes, nonViable, empty,
                         emptyDestination) + (emptyDestination - 1) * 5
    )


lineRegex = re.compile(
    r"^/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)")


def getInput(filePath: str) -> FileSystem:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        fileSystem = FileSystem()
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                fileSystem[int(match.group("x")) + int(match.group("y")) * 1j] = \
                    (int(match.group("size")), int(match.group("used")))
        return fileSystem


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
