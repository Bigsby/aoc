#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple, Union
from enum import Enum
from itertools import cycle
import copy


class MapItemType(Enum):
    Straight = 0
    Turn = 1
    Intersection = 2


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1


Position = complex
Direction = complex
Straight = Tuple[MapItemType,Orientation]
Turn = Tuple[MapItemType,Tuple[Direction,Direction]]
Intersection = Tuple[MapItemType,int]
Map = Dict[Position,Union[Straight,Turn,Intersection]]


DIRECTION_CHANGES = [ 1j, 1, -1j ]
class Train():
    def __init__(self, position: Position, direction: Direction):
        self.position = position
        self.direction = direction
        self.directionCycle = cycle(DIRECTION_CHANGES)
    
    def tick(self):
        self.position += self.direction

    def turn(self):
        self.direction *= next(self.directionCycle)


TRAIN_CHAR = {
    1: ">",
    -1: "<",
    1j: "^",
    -1j: "v"
}
TURN_CHAR = {
    (1, 1j): "\\",
    (1, -1j): "/",
    (-1, 1j): "/",
    (-1, -1j): "\\"
}
def showMapArea(mapItems: Map, start: Position, end: Position, trains: List[Train]):
    for y in range(int(start.imag), int(end.imag) - 1, -1):
        for x in range(int(start.real), int(end.real) + 1):
            position = x + y * 1j
            c = " "
            if position in mapItems:
                mapItem = mapItems[position]
                if mapItem[0] == MapItemType.Straight:
                    c = "-" if mapItem[1] == Orientation.Horizontal else "|"
                elif mapItem[0] == MapItemType.Intersection:
                    c = "+"
                elif mapItem[0] == MapItemType.Turn:
                    c = TURN_CHAR[mapItem[1]]
            train = next(filter(lambda train: train.position == position, trains), None)
            if train:
                c = TRAIN_CHAR[train.direction]
            print(c, end="")
        print()
    print()


def showTrain(mapItems: Map, train: Train, trains: List[Train]):
    offset = 40
    maxX = max(map(lambda p: p.real, mapItems.keys()))
    maxY = min(map(lambda p: p.imag, mapItems.keys()))
    startX = max(0, int(train.position.real) - offset)
    endX = min(maxX, int(train.position.real) + offset)
    startY = min(0, int(train.position.imag) + offset)
    endY = max(maxY, int(train.position.imag) - offset)
    showMapArea(mapItems, startX + startY * 1j, endX + endY * 1j, trains)


def positionToString(position: Position) -> str:
    return f"{int(position.real)},{abs(int(position.imag))}"


def solve(mapTrains: Tuple[Map,List[Train]]) -> Tuple[str,str]:
    mapItems, trains = mapTrains
    trains = copy.deepcopy(trains)
    trainLocations = { train.position: train for train in trains }
    part1Result = ""
    while True:
        for position in sorted(list(trainLocations.keys()), key=lambda position: (-position.imag, position.real)):
            if position not in trainLocations:
                continue
            train = trainLocations[position]
            del trainLocations[position]
            train.tick()
            if train.position in trainLocations:
                if not part1Result:
                    part1Result = positionToString(train.position)
                del trainLocations[train.position]    
            else:
                trainLocations[train.position] = train
            mapItem = mapItems[train.position]
            if mapItem[0] == MapItemType.Intersection:
                train.turn()
            elif mapItem[0] == MapItemType.Turn:
                train.direction = mapItem[1][1] if train.direction.real else mapItem[1][0]
        if len(trainLocations) == 1:
                return part1Result, positionToString(list(trainLocations.keys())[0])


TRAINS = {
    ">": 1,
    "<": -1,
    "^": 1j,
    "v": -1j
}
TURNS = [ "/", "\\" ]
TURN_DIRECTIONS = {
    " /": (1, -1j),
    "-/": (-1, 1j),
    "+/": (-1, 1j),
    "-\\": (-1, -1j),
    "+\\": (-1, -1j),
    " \\": (1, 1j),
}
STRAIGHTS = { 
    "-": Orientation.Horizontal,
    "|": Orientation.Vertical
}
INTERSECTION = "+"
def getInput(filePath: str) -> Tuple[Map,List[Train]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        trains: List[Train] = []
        map: Map = {}
        previousC = " "
        trainPositionToFillIn = []
        trainIndex = 0
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                position = x - y * 1j
                if c == INTERSECTION:
                    map[position] = (MapItemType.Intersection,0)
                elif c in STRAIGHTS:
                    map[position] = (MapItemType.Straight, STRAIGHTS[c])
                elif c in TURNS:
                    if previousC not in [ "-", "+" ]:
                        previousC = " "
                    map[position] = (MapItemType.Turn,TURN_DIRECTIONS[previousC + c])
                elif c in TRAINS:
                    trains.append(Train(position, TRAINS[c]))
                    trainIndex += 1
                    trainPositionToFillIn.append(position)       
                previousC = c
        
        for position in trainPositionToFillIn:
            for direction in TRAINS.values():
                if position + direction in map:
                    mapPosition = map[position + direction]
                    if mapPosition[0] == MapItemType.Straight:
                        map[position] = mapPosition
                    elif mapPosition[0] == MapItemType.Intersection:
                        map[position] = (MapItemType.Straight,Orientation.Horizontal if direction.real else Orientation.Vertical)
        return map, trains


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