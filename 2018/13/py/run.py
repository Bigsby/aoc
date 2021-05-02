#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from enum import Enum
from itertools import cycle

Position = complex
Direction = complex


class Orientation(Enum):
    Horizontal = 0
    Vertical = 1


class MapItem:
    pass


class Straight(MapItem):
    def __init__(self, orientation: Orientation) -> None:
        self.orientation = orientation


class Turn(MapItem):
    def __init__(self, directions: Tuple[Direction, Direction]) -> None:
        self.directions = directions
        self.vertical = directions[1]
        self.horizontal = directions[0]


class Intersection(MapItem):
    pass


Map = Dict[Position, MapItem]


class Train():
    DIRECTION_CHANGES = [1j, 1, -1j]

    def __init__(self, position: Position, direction: Direction):
        self.position = position
        self.direction = direction
        self.direction_cycle = cycle(Train.DIRECTION_CHANGES)

    def tick(self):
        self.position += self.direction

    def turn(self):
        self.direction *= next(self.direction_cycle)


TRAIN_CHAR = {
    1: ">",
    -1: "<",
    1j: "^",
    -1j: "v"
}
TURN_CHAR: Dict[Tuple[Direction, Direction], str] = {
    (1, 1j): "\\",
    (1, -1j): "/",
    (-1, 1j): "/",
    (-1, -1j): "\\"
}


def show_map_area(map_items: Map, start: Position, end: Position, trains: List[Train]):
    for y in range(int(start.imag), int(end.imag) - 1, -1):
        for x in range(int(start.real), int(end.real) + 1):
            position = x + y * 1j
            c = " "
            if position in map_items:
                map_item = map_items[position]
                if isinstance(map_item, Straight):
                    c = "-" if map_item.orientation == Orientation.Horizontal else "|"
                elif isinstance(map_item, Intersection):
                    c = "+"
                elif isinstance(map_item, Turn):
                    c = TURN_CHAR[map_item.directions]
            train = next(
                filter(lambda train: train.position == position, trains), None)
            if train:
                c = TRAIN_CHAR[train.direction]
            print(c, end="")
        print()
    print()


def show_train(map_items: Map, train: Train, trains: List[Train]):
    offset = 40
    max_x = max(map(lambda p: p.real, map_items.keys()))
    max_y = min(map(lambda p: p.imag, map_items.keys()))
    start_x = max(0, int(train.position.real) - offset)
    end_x = min(max_x, int(train.position.real) + offset)
    start_y = min(0, int(train.position.imag) + offset)
    end_y = max(max_y, int(train.position.imag) - offset)
    show_map_area(map_items, start_x + start_y *
                  1j, end_x + end_y * 1j, trains)


def position_to_string(position: Position) -> str:
    return f"{int(position.real)},{abs(int(position.imag))}"


def solve(data: Tuple[Map, List[Train]]) -> Tuple[str, str]:
    map_items, trains = data
    train_locations = {train.position: train for train in trains}
    part1_result = ""
    cycles = 0
    while True:
        cycles += 1
        for position in sorted(list(train_locations.keys()), key=lambda position: (-position.imag, position.real)):
            if position not in train_locations:
                continue
            train = train_locations[position]
            del train_locations[position]
            train.tick()
            if train.position in train_locations:
                if not part1_result:
                    part1_result = position_to_string(train.position)
                del train_locations[train.position]
            else:
                train_locations[train.position] = train
            map_item = map_items[train.position]
            if isinstance(map_item, Intersection):
                train.turn()
            elif isinstance(map_item, Turn):
                train.direction = map_item.vertical if train.direction.real else map_item.horizontal
        if len(train_locations) == 1:
            return part1_result, position_to_string(list(train_locations.keys())[0])


TRAINS = {
    ">": 1,
    "<": -1,
    "^": 1j,
    "v": -1j
}
TURNS = ["/", "\\"]
TURN_DIRECTIONS = {
    " /": (1, -1j),
    "-/": (-1, 1j),
    ">/": (-1, 1j),
    "</": (-1, 1j),
    "+/": (-1, 1j),
    "-\\": (-1, -1j),
    ">\\": (-1, -1j),
    "<\\": (-1, -1j),
    "+\\": (-1, -1j),
    " \\": (1, 1j),
}
STRAIGHTS = {
    "-": Orientation.Horizontal,
    "|": Orientation.Vertical
}
INTERSECTION = "+"


def get_input(file_path: str) -> Tuple[Map, List[Train]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        trains: List[Train] = []
        map: Map = {}
        previous_c = " "
        train_position_to_fill_in: List[complex] = []
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                position = x - y * 1j
                if c == INTERSECTION:
                    map[position] = Intersection()
                elif c in STRAIGHTS:
                    map[position] = Straight(STRAIGHTS[c])
                elif c in TURNS:
                    if previous_c not in ["-", "+", "<", ">"]:
                        previous_c = " "
                    map[position] = Turn(TURN_DIRECTIONS[previous_c + c])
                elif c in TRAINS:
                    trains.append(Train(position, TRAINS[c]))
                    train_position_to_fill_in.append(position)
                previous_c = c
        for position in train_position_to_fill_in:
            for direction in TRAINS.values():
                if position + direction in map:
                    map_position = map[position + direction]
                    if isinstance(map_position, Straight):
                        map[position] = map_position
                    elif isinstance(map_position, Intersection):
                        map[position] = Straight(
                            Orientation.Horizontal if direction.real else Orientation.Vertical)
        return map, trains


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
