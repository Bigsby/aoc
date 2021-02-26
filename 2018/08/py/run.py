#! /usr/bin/python3

import sys, os, time
from typing import Any, List, Tuple

Node = Tuple[List['Node'],List[int]]


def readNode(data: List[int]) -> Node:
    childrenCount = data.pop()
    metadataCount = data.pop()
    node = ([],[])
    for _ in range(childrenCount):
        node[0].append(readNode(data))
    for _ in range(metadataCount):
        node[1].append(data.pop())
    return node


def getMetadataSum(node: Node) -> int:
    return sum(node[1]) + sum(map(lambda child: getMetadataSum(child), node[0]))


def getRoot(data: List[int]) -> Node:
    data = list(data)
    data.reverse()
    return readNode(data)


def getValue(node: Tuple[List[Any],List[int]]) -> int:
    if not node[0]:
        return sum(node[1])
    childrenCount = len(node[0])
    return sum(map(lambda index: getValue(node[0][index - 1]) if index > 0 and index <= childrenCount else 0, node[1]))


def solve(data: List[int]) -> Tuple[int,int]:
    root = getRoot(data)
    return (
        getMetadataSum(root),
        getValue(root)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().strip().split(" ") ]


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