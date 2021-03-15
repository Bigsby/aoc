#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
import re
from itertools import combinations


Floor = List[int]
Floors = List[Floor]
Elevator = Tuple[int, int]
Move = Tuple[int, int, Elevator]
State = Tuple[int, Floors]
EMPTY_SLOT = 0
radioisotopes: Dict[str, int] = {}


def print_state(state: State):
    print(state[0])
    for floor in state[1]:
        print(floor)


def is_group_valid(group: Iterable[int]) -> bool:
    test_group = list(group)
    generators = [part for part in group if part > 0]
    for generator in generators:
        if -generator in test_group:
            test_group.remove(-generator)
            test_group.remove(generator)
    return not test_group or any(map(lambda part: part > 0, test_group)) ^ any(map(lambda part: part < 0, test_group))


def is_move_valid(current_floor: Floor, next_floor: Floor, elevator: Elevator) -> bool:
    current_test_floor = list(current_floor)
    for part in elevator:
        if part in current_test_floor:
            current_test_floor.remove(part)
    next_test_floor = list(next_floor)
    for part in elevator:
        if part != EMPTY_SLOT:
            next_test_floor.append(part)
    return is_group_valid(current_test_floor) and is_group_valid(next_test_floor)


def make_move(floors: Floors, move: Move) -> State:
    floors = [list(floor) for floor in floors]
    current_floor, next_floor, parts = move
    for part in parts:
        if part != EMPTY_SLOT:
            floors[current_floor].remove(part)
            floors[next_floor].append(part)
    return next_floor, floors


def get_valid_directional_moves(state: State, direction: int, possible_moves_groups: List[Elevator]) -> List[Move]:
    current_floor, floors = state
    next_floor = current_floor + direction
    valid_moves: List[Move] = []
    if (next_floor < 0 or next_floor == len(floors)) \
            or (next_floor == 0 and not len(floors[next_floor])) \
            or (next_floor == 1 and not (len(floors[1]) or len(floors[0]))):
        return []
    for move_group in possible_moves_groups:
        if is_move_valid(floors[current_floor], floors[next_floor], move_group):
            valid_moves.append((current_floor, next_floor, move_group))
    return valid_moves


def prune_moves(moves: List[Move]) -> List[Move]:
    pair_moves = [move for move in moves if move[2][0] == -move[2][1]]
    if len(pair_moves) > 1:
        for pair_move in pair_moves[:-1]:
            moves.remove(pair_move)
    upstairs_moves = [move for move in moves if move[0] < move[1]]
    single_up_moves = [move for move in upstairs_moves if move[2]
                     [0] == EMPTY_SLOT or move[2][1] == EMPTY_SLOT]
    if len(single_up_moves) != len(upstairs_moves):
        for singleUpMove in single_up_moves:
            moves.remove(singleUpMove)
    downstairs_moves = [move for move in moves if move[0] > move[1]]
    pair_downstairs_moves = [move for move in downstairs_moves if move[2]
                           [0] != EMPTY_SLOT and move[2][1] != EMPTY_SLOT]
    if len(pair_downstairs_moves) != len(downstairs_moves):
        for pair_downstairs_move in pair_downstairs_moves:
            moves.remove(pair_downstairs_move)
    return moves


def get_valid_moves(state: State) -> List[Move]:
    current_floor, floors = state
    possible_move_groups = list(
        filter(is_group_valid, combinations(floors[current_floor] + [EMPTY_SLOT], 2)))
    valid_moves: List[Move] = get_valid_directional_moves(state, 1, possible_move_groups) \
        + get_valid_directional_moves(state, -1, possible_move_groups)
    return prune_moves(valid_moves)


def solve_floors(floors: Floors) -> int:
    queue: List[Tuple[State, int]] = [((0, floors), 0)]
    radioisotopes_count = max(max(floor) if floor else 0 for floor in floors)
    while queue:
        state, moves_count = queue.pop()
        print_state(state); input()
        for move in get_valid_moves(state):
            new_state = make_move(state[1], move)
            new_current, new_floors = new_state
            if new_current == len(floors) - 1 and len(new_floors[-1]) == radioisotopes_count * 2:
                return moves_count + 1
            else:
                queue.append((new_state, moves_count + 1))
    raise Exception("Solution not found")


line_regex = re.compile(
    r"a (?P<radioisotope>\w+)(?P<part>-compatible microchip| generator)")


def parse_line(line: str) -> Floor:
    result: List[int] = []
    for match in line_regex.finditer(line):
        radioisotope = match.group("radioisotope")
        if not radioisotopes:
            radioisotopes[radioisotope] = 1
        elif radioisotope not in radioisotopes:
            radioisotopes[radioisotope] = max(radioisotopes.values()) + 1
        value = radioisotopes[radioisotope]
        result.append(value if "generator" in match.group("part") else -value)
    return result


PART2_EXTRA = "a elerium generator, a elerium-compatible microchip, a dilithium generator, a dilithium-compatible microchip"


def solve(floors: Floors) -> Tuple[int, int]:
    part1_result = solve_floors(floors)
    floors[0] += parse_line(PART2_EXTRA)
    return (
        part1_result,
        solve_floors(floors)
    )


def get_input(file_path: str) -> Floors:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


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
