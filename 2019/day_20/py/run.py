#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple, Set

Position = complex
LevelPosition = Tuple[Position,int]
Maze = List[Position]
Portals = Dict[Position,str]
DIRECTIONS = [ 1j, -1j, 1, -1 ]


def part1(data: Tuple[Maze,Portals,Position,Position]) -> int:
    maze, portals, start, end = data
    visited = { start }
    queue: List[Tuple[Position,List[Position]]] = [(start, [ start ])]
    while queue:
        position, path = queue.pop(0)
        newPositions = []
        if position in portals:
            newPositions.append(next(p for p, label in portals.items() if label == portals[position] and p != position))
        for direction in DIRECTIONS:
            newPositions.append(position + direction)
        for newPosition in newPositions:
            if newPosition == end:
                return len(path)
            if newPosition not in visited and newPosition in maze:
                newPath = path[:]
                visited.add(newPosition)
                newPath.append(newPosition)
                queue.append((newPosition, newPath))
        
    raise Exception("Path not found")


def part2(data: Tuple[Maze,Portals,Position,Position]) -> int:
    maze, portals, start, end = data
    minX = min(p.real for p in maze)
    maxX = max(p.real for p in maze)
    minY = min(p.imag for p in maze)
    maxY = max(p.imag for p in maze)
    outerPortals = { position: label for position, label in portals.items() \
        if position.real == minX or position.real == maxX or \
            position.imag == minY or position.imag == maxY }
    innerPortals = { position: label for position, label in portals.items() if position not in outerPortals }
    reverseOuterPortals = { label: position for position, label in outerPortals.items() }
    reverseInnerPortals = { label: position for position, label in innerPortals.items() }
    endPosition = (end, 0)
    startPosition = (start, 0)

    visited: Set[LevelPosition] = { startPosition }
    queue: List[Tuple[LevelPosition,List[LevelPosition]]] = [ (startPosition, [ startPosition ])]
    while queue:
        (position, level), path = queue.pop(0)
        newPositions = []
        if position in innerPortals:
            newPositions.append((reverseOuterPortals[innerPortals[position]], level + 1))
        elif level != 0 and position in outerPortals:
            newPositions.append((reverseInnerPortals[outerPortals[position]], level - 1))
        for direction in DIRECTIONS:
            newPositions.append((position + direction, level))
        for newPosition in newPositions:
            if newPosition == endPosition:
                return len(path)
            if newPosition not in visited and newPosition[0] in maze:
                newPath = path[:]
                visited.add(newPosition)
                newPath.append(newPosition)
                queue.append((newPosition, newPath))
        
    raise Exception("Path not found")


def getInput(filePath: str) -> Tuple[Maze,Portals,Position,Position]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        maze = []
        portals = {}
        start = 0j
        end = 0j
        lines = file.readlines()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                position = x + y * 1j
                if c == ".":
                    maze.append(position)
                    portal = ""
                    if lines[y - 1][x].isalpha():
                        portal = lines[y - 2][x] + lines[y - 1][x]
                    elif lines[y + 1][x].isalpha():
                        portal = lines[y + 1][x] + lines[y + 2][x]
                    elif line[x - 1].isalpha():
                        portal = lines[y][x - 2] + line[x - 1]
                    elif line[x + 1].isalpha():
                        portal = line[x + 1] + line[x + 2]
                    if portal:
                        if portal == "AA":
                            start = position
                        elif portal == "ZZ":
                            end = position
                        else:
                            portals[position] = portal
        
        return maze, portals, start, end



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