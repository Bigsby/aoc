#! /usr/bin/python3

import sys, os, time
from typing import Dict, FrozenSet, List, Set, Tuple
from collections import defaultdict
from heapq import heappop, heappush

Position = complex
Maze = List[Position]
KeysDoors = Dict[Position,str]
Keys = KeysDoors
Doors = KeysDoors
Path = List[Position]


def showMaze(maze: Maze, keysDoors: KeysDoors, starts: List[Position]):
    maxX = int(max(p.real for p in maze))
    maxY = int(max(p.imag for p in maze))
    for y in range(maxY + 1):
        for x in range(maxX + 1):
            c = "."
            current = x + y * 1j
            if current in maze:
                c = "#"
            if current in keysDoors:
                c = keysDoors[current]
            if current in starts:
                c = "@"
            print(c, end="")
        print()
    print()


DIRECTIONS = [ -1, -1j, 1, 1j ]
def findPathsFromPosition(maze: Maze, keysDoors: KeysDoors, start: Position) -> Dict[str,Tuple[int,Set[str]]]:
    visited = { start }
    queue: List[Tuple[Position,int,Set[str]]] = [ (start, 0, set()) ]
    paths: Dict[str,Tuple[int,Set[str]]] = {}
    while queue: 
        position, distance, requiredKeys = queue.pop(0)
        for direciton in DIRECTIONS:
            newPosition = position + direciton
            if newPosition not in maze and newPosition not in visited:
                visited.add(newPosition)
                newRequiredKeys = set(requiredKeys)
                if newPosition in keysDoors:
                    keyDoor = keysDoors[newPosition]
                    if keyDoor.islower():
                        paths[keyDoor] = distance + 1, requiredKeys
                    else:
                        newRequiredKeys.add(keyDoor.lower())
                queue.append((newPosition, distance + 1, newRequiredKeys))
    return paths


def findShortestPathFromKeyGragph(pathsFromKeys: Dict[str,Dict[str,Tuple[int,Set[str]]]], keys: Dict[str,Position], entrances: List[str]) -> int:
    paths: List[Tuple[int,Tuple[str,...], FrozenSet[str]]] = [(0, tuple(entrances), frozenset())]
    visited: Dict[Tuple[Tuple[str,...], FrozenSet[str]],int] = defaultdict(int)
    while paths:
        distance, currentPoints, keysFound = heappop(paths)
        if len(keysFound) == len(keys.keys()):
            return distance
        for curr_idx, curr_key in enumerate(currentPoints):
            for next_key, next_path in pathsFromKeys[curr_key].items():
                if next_key not in keysFound:
                    next_keys = frozenset(keysFound | {next_key})
                    next_pos = currentPoints[:curr_idx] + (next_key,) + currentPoints[curr_idx + 1:]
                    node_id = (next_pos, next_keys)
                    dist = distance + next_path[0]
                    if (node_id not in visited or visited[node_id] > dist) and len(next_path[1] - keysFound) == 0:
                        heappush(paths, (dist, next_pos, next_keys))
                        visited[node_id] = dist
    raise Exception("Path not found")


def findShortestPath(maze: Maze, keysDoors: KeysDoors, entrances: List[Position]) -> int:
    keys = { keyDoor: position for position, keyDoor in keysDoors.items() if keyDoor.islower() }
    keysPaths = { key: findPathsFromPosition(maze, keysDoors, position) for key, position in keys.items() }
    for index, position in enumerate(entrances):
        keysPaths[str(index)] = findPathsFromPosition(maze, keysDoors, position)
    return findShortestPathFromKeyGragph(keysPaths, keys, [str(index) for index, _ in enumerate(entrances)])


def part1(data: Tuple[Maze,KeysDoors,Position]) -> int:
    maze, keysDoors, entrance = data
    return findShortestPath(maze, keysDoors, [ entrance])


def part2(data: Tuple[Maze,KeysDoors,Position]) -> int:
    maze, keysDoors, start = data
    for offset in [ -1, -1j, 0, 1, 1j]:
        maze.append(start + offset)
    entrances = [ start + offset for offset in [ -1 - 1j, 1 - 1j, -1 + 1j, 1 + 1j ]]
    return findShortestPath(maze, keysDoors, entrances)


def getInput(filePath: str) -> Tuple[Maze,KeysDoors,Position]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        maze: Maze = []
        keysDoors: KeysDoors = {}
        entrance = 0j
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "#":
                    maze.append(x + y * 1j)
                elif c == "@":
                    entrance = x + y * 1j
                elif c != ".":
                    keysDoors[x + y * 1j] = c
        return maze, keysDoors, entrance


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