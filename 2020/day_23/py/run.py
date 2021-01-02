#! /usr/bin/python3

import sys, os, time


class Node:
    def __init__(self, value):
        self.next = None
        self.value = value


def buildLinkedList(cups):
    start = previous = last = Node(cups[0])
    values = [None] * len(cups)
    values[start.value - 1] = start
    for cup in cups[1:]:
        last = Node(cup)
        previous.next = last
        values[last.value - 1] = last
        previous = last
    last.next = start
    return start, values


def playGame(cups, moves):
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


def part1(cups):
    oneNode = playGame(cups, 100)
    result = []
    currentNode = oneNode.next
    while currentNode.value != 1:
        result.append(currentNode.value)
        currentNode = currentNode.next
    return "".join(map(str, result))


def part2(cups):
    cups += [ *range(10, 10**6 + 1) ]
    oneNode = playGame(cups, 10**7)
    return oneNode.next.value * oneNode.next.next.value


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(c) for c in file.read().strip() ]


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