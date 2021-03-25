#! /usr/bin/python3

import sys
import os
import time
from typing import Iterable, List, Set, Tuple
import re


Position = complex
ClaySquares = List[Position]
Water = Set[Position]
Spring = Position


def getEdges(positions: Iterable[Position]) -> Tuple[int, int, int, int]:
    return int(min(map(lambda s: s.real, positions))), \
        int(max(map(lambda s: s.real, positions))), \
        int(min(map(lambda s: s.imag, positions))), \
        int(max(map(lambda s: s.imag, positions)))


def printArea(clay: ClaySquares, flowing: Water, settled: Water, spring: Spring, queue: List[Position], all: bool = False):
    minX, maxX, minY, maxY = getEdges(
        clay + list(settled) + list(flowing) + [spring])
    margins = 20
    if not all:
        minX = max(int(spring.real) - margins * 2, minX)
        maxX = min(int(spring.real) + margins * 2, maxX)
        minY = max(int(spring.imag) - margins, minY)
        maxY = min(int(spring.imag) + margins, maxY)
    for y in range(minY, maxY + margins + 1):
        for x in range(minX - margins, maxX + margins + 1):
            c = " "
            position = x + y * 1j
            if position in clay:
                c = "#"
            if position in flowing:
                c = "|"
            if position in settled:
                c = "~"
            if position in queue:
                c = "q"
            if position == spring:
                c = "+"
            print(c, end="")
        print()
    print()


def findEdge(spring: Position, direction: int, settled: Water, clay: ClaySquares) -> Tuple[int, bool]:
    x = direction
    while True:
        current = spring + x
        if current in clay:
            return x - direction, False
        below = current + 1j
        if below not in clay and below not in settled:
            return x, True
        x += direction


def solve(clay: ClaySquares) -> Tuple[int, int]:
    maxY = int(max(map(lambda s: s.imag, clay)))
    minY = int(min(map(lambda s: s.imag, clay)))
    settled = Water()
    flowing = Water()
    queue = [500 + minY * 1j]
    while queue:
        spring = queue.pop()
        below = spring + 1j
        if below in flowing:
            continue
        flowing.add(spring)
        while below.imag <= maxY and below not in clay and below not in settled:
            flowing.add(below)
            below += 1j
        if below in clay or below in settled:
            x, y = int(below.real), below.imag * 1j - 1j
            leftOffset, leftOverflown = findEdge(below - 1j, -1, settled, clay)
            rightOffset, rightOverflown = findEdge(
                below - 1j, 1, settled, clay)
            isOverflown = leftOverflown or rightOverflown
            if not isOverflown:
                queue.append(below - 2j)
            for levelX in range(x + leftOffset, x + rightOffset + 1):
                position = levelX + y
                if isOverflown:
                    flowing.add(position)
                else:
                    settled.add(position)
                    if position in flowing:
                        flowing.remove(position)
                    if position in queue:
                        queue.remove(position)
            if leftOverflown:
                queue.append(x + leftOffset + y)
            if rightOverflown:
                queue.append(x + rightOffset + y)
    return len(settled) + len(flowing), len(settled)


lineRegex = re.compile(
    r"^(?P<sC>x|y)=(?P<sV>\d+), (?:x|y)=(?P<mS>\d+)..(?P<mE>\d+)$")


def parseLine(line: str) -> ClaySquares:
    match = lineRegex.match(line)
    if match:
        result = ClaySquares()
        sC, sV, mS, mE = match.group("sC"), int(match.group("sV")), int(
            match.group("mS")), int(match.group("mE"))
        if sC == "x":
            for y in range(mS, mE + 1):
                result.append(sV + y * 1j)
        else:
            for x in range(mS, mE + 1):
                result.append(x + sV * 1j)
        return result
    raise Exception("Bad format", line)


def getInput(filePath: str) -> ClaySquares:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        clay = ClaySquares()
        for line in file.readlines():
            clay += parseLine(line)
        return clay


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
