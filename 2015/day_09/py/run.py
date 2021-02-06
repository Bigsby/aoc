#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


class Edge():
    def __init__(self, nodeA: str, nodeB: str, distance: str):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.distance = int(distance)


def getSingleNodes(edges: List[Edge]) -> List[str]:
    nodes = set()
    for path in edges:
        nodes.add(path.nodeA)
        nodes.add(path.nodeB)
    return list(nodes)


def getShortestPath(edges: List[Edge], longest: bool) -> int:
    singleNodes = getSingleNodes(edges)
    length = len(singleNodes)
    stack: List[Tuple[List[str],str,int]] = [ ([ node ], node, 0) for node in singleNodes ]
    bestDistance = 0 if longest else sys.maxsize
    while stack:
        path, current, distance = stack.pop()
        for edge in filter(lambda edge: edge.nodeA == current or edge.nodeB == current, edges):
            nextNode = edge.nodeB if current == edge.nodeA else edge.nodeA
            if nextNode in path:
                continue
            newPath = list(path)
            newPath.append(nextNode)
            newDistance = distance + edge.distance
            if not longest and newDistance > bestDistance:
                continue
            if len(newPath) == length:
                bestDistance = max(bestDistance, newDistance) if longest else min(bestDistance, newDistance)
            else:
                stack.append((newPath, nextNode, newDistance))
    return bestDistance
 

def part1(edges: List[Edge]) -> int:
    return getShortestPath(edges, False)


def part2(edges: List[Edge]) -> int:
    return getShortestPath(edges, True)


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()