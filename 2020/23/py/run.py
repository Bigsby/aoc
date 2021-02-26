#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


class Node:
    def __init__(self, value: int):
        self.next = self
        self.value = value


def buildLinkedList(cups: List[int]) -> Tuple[Node,List[Node]]:
    start = previous = last = Node(cups[0])
    values = [start] * len(cups)
    values[start.value - 1] = start
    for cup in cups[1:]:
        last = Node(cup)
        previous.next = last
        values[last.value - 1] = last
        previous = last
    last.next = start
    return start, values


def playGame(cups: List[int], moves: int) -> Node:
    start, values = buildLinkedList(cups)
    maxValue = max(cups)
    current = start
    while moves:
        moves -= 1
        firstRemoved = current.next
        lastRemoved = firstRemoved.next.next
        removedValues = {firstRemoved.value, firstRemoved.next.value, lastRemoved.value}
        current.next = lastRemoved.next
        destinationValue = current.value - 1
        while destinationValue in removedValues or destinationValue < 1:
            destinationValue -= 1
            if destinationValue < 0:
                destinationValue = maxValue
                
        destinationLink = values[destinationValue - 1]
        lastRemoved.next = destinationLink.next
        destinationLink.next = firstRemoved
        current = current.next
    return values[0]


def part1(cups: List[int]) -> str:
    oneNode = playGame(cups, 100)
    result = []
    currentNode = oneNode.next
    while currentNode.value != 1:
        result.append(currentNode.value)
        currentNode = currentNode.next
    return "".join(map(str, result))


def part2(cups: List[int]) -> int:
    cups += [ *range(10, 10**6 + 1) ]
    oneNode = playGame(cups, 10**7)
    return oneNode.next.value * oneNode.next.next.value


def solve(cups: List[int]) -> Tuple[str,int]:
    return (
        part1(cups),
        part2(cups)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(c) for c in file.read().strip() ]


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