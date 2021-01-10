#! /usr/bin/python3

import sys, os, time
from typing import Iterator, List, Tuple
import re
from itertools import permutations


class Edge():
    def __init__(self, nodeA: str, nodeB: str, distance: str):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.distance = int(distance)


def getPathDistance(permutation: Tuple[str,...], paths: List[Edge]) -> int:
    distance = 0
    for index in range(0, len(permutation) - 1):
        path = next(filter(lambda p: p.nodeA == permutation[index] and p.nodeB == permutation[index + 1] or p.nodeA == permutation[index + 1] and p.nodeB == permutation[index], paths))
        distance = distance + path.distance
    return distance


def getSingleNodes(edges: List[Edge]) -> List[str]:
    nodes: List[str] = []
    for path in edges:
        nodes.append(path.nodeA)
        nodes.append(path.nodeB)
    return list(set(nodes))
 

def getPossiblePaths(nodes: List[str]) -> Iterator[Tuple[str,...]]:
    return permutations(nodes, len(nodes))


def getMinOrMax(edges: List[Edge], getMax: bool = False) -> int:
    singleNodes = getSingleNodes(edges)
    possiblePaths = getPossiblePaths(singleNodes)
    if getMax:
        return max(map(lambda permutation: getPathDistance(permutation, edges), possiblePaths))
    return min(map(lambda permutation: getPathDistance(permutation, edges), possiblePaths))


def part1(edges: List[Edge]):
    return getMinOrMax(edges)


def part2(edges: List[Edge]):
    return getMinOrMax(edges, True)


lineRegex = re.compile(r"^(.*)\sto\s(.*)\s=\s(\d+)$")
def parseLine(line: str) -> Edge:
    match = lineRegex.match(line)
    if match:
        return Edge(match.group(1), match.group(2), match.group(3))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Edge]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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