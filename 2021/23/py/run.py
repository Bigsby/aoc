#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
from collections import defaultdict

State = str
Input = State

EMPTY = "."
A = ord('A')

def get_letter_cost(letter: str) -> int:
    return 10 ** (ord(letter) - A)


def get_letter_room(letter: str) -> int:
    return ord(letter) - A


def new_state(state: State, a: int, b: int) -> State:
    return state[:a] + state[b] + state[a + 1:b] + state[a] + state[b + 1:]


def move_to_room(state: State, cost: int, room_depth) -> Tuple[State, int]:
    for corridor_position in range(7):
        if state[corridor_position] == EMPTY:
            continue
        position = corridor_position
        letter = state[position]
        room = get_letter_room(letter)
        offset = 7 + room * room_depth
        row = room_depth - 1
        while row > 0 and state[offset + row] == letter:
            row -= 1
        if state[offset + row] != EMPTY:
            continue
        letter_cost = get_letter_cost(letter)
        added_cost = (2 + row) * letter_cost
        while position < room + 1 and state[position + 1] == EMPTY:
            added_cost += letter_cost * 2 if position > 0 else letter_cost
            position += 1
        while position > room + 2 and state[position - 1] == EMPTY:
            added_cost += letter_cost * 2 if position < 6 else letter_cost
            position -= 1
        if position != room + 1 and position != room + 2:
            continue
        return move_to_room(new_state(state, corridor_position, offset + row), cost + added_cost, room_depth)
    return (state, cost)


def move_to_corridor(state: State, room_depth: int) -> List[Tuple[State, int]]:
    new_states = []
    for room in range(4):
        offset = 7 + room * room_depth
        row = 0
        while row < room_depth and state[offset + row] == EMPTY:
            row += 1
        if row == room_depth:
            continue
        letter = state[offset + row]
        if room == get_letter_room(letter) and (row == room_depth - 1 or all(state[i] == letter for i in range(offset + row + 1, offset + room_depth))):
            continue
        position = room + 2
        letter_cost = get_letter_cost(letter)
        added_cost = letter_cost * row
        while position < 7 and state[position] == EMPTY:
            added_cost += 2 * letter_cost if position < 6 else letter_cost
            new_states.append(move_to_room(new_state(state, position, offset + row), added_cost, room_depth))
            position += 1
        position = room + 1
        added_cost = letter_cost * row
        while position >= 0 and state[position] == EMPTY:
            added_cost += 2 * letter_cost if position > 0 else letter_cost
            new_states.append(move_to_room(new_state(state, position, offset + row), added_cost, room_depth))
            position -= 1
    return new_states


def find_cost(start: State) -> int:
    room_depth = (len(start) - 7) // 4
    queue = defaultdict(list) 
    queue[0].append(start)
    costs = {start: 0}
    cost = 0
    while True:
        for state in queue[cost]:
            if costs[state] < cost:
                continue
            new_states = move_to_corridor(state, room_depth)
            if all(state[i] == EMPTY for i in range(7)) and len(new_states) == 0:
                return cost
            for (new_state , new_cost) in new_states:
                if new_state in costs and costs[new_state] <= cost + new_cost:
                    continue
                costs[new_state]=cost + new_cost
                queue[cost + new_cost].append(new_state)
        cost += 1


def part2(puzzle_input: Input) -> int:
    state = puzzle_input[:8]
    state += "DD"
    state += puzzle_input[8:10]
    state += "CB"
    state += puzzle_input[10:12]
    state += "BA"
    state += puzzle_input[12:14]
    state += "AC"
    state += puzzle_input[14]
    return find_cost(state)


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (find_cost(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        lines = file.read().splitlines()
        state = "." * 7
        for x in [ 3, 5, 7, 9 ]:
            for y in [ 2, 3 ]:
                state += lines[y][x]
        return state


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
