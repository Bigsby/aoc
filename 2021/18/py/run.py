#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List
OPEN = -1
CLOSE = -2

Number = List[int]
Input = List[Number]


def get_next_number(number: Number, index: int, direction:int) -> int:
    while index > 0 and index < len(number):
        if number[index] >= 0:
            return index
        index += direction
    return -1


def explode(number: Number) -> Tuple[Number, bool]:
    nest = 0
    for index in range(len(number)):
        if number[index] == OPEN:
            nest += 1
            if nest == 5:
                left_number_index = get_next_number(number, index, -1)
                right_number_index = get_next_number(number, index + 3, 1)
                if left_number_index > 0:
                    number[left_number_index] += number[index + 1]
                if right_number_index > 0:
                    number[right_number_index] += number[index + 2]
                number = number[:index] + [0] + number[index + 4:]
                return number, True
        elif number[index] == CLOSE:
            nest -= 1
    return number, False


def split(number: Number) -> Tuple[Number, bool]:
    for index in range(len(number)):
        if number[index] > 9:
            left = number[index] // 2
            right = number[index] - left
            number = number[:index] + [ OPEN, left, right, CLOSE] + number[index + 1:]
            return number, True
    return number, False


def reduce(number: Number) -> Number:
    nest = 0
    changed = True
    while changed:
        changed = False
        number, changed = explode(number)
        if not changed:
            number, changed = split(number)
    return number


def get_magnitude(number: Number) -> int:
    while len(number) > 1:
        for index in range(len(number)):
            if number[index] >= 0 and number[index + 1] >= 0:
                number = number[:index - 1] + [ number[index] * 3 + number[index + 1] * 2 ] + number[index + 3:]
                break
    return number[0]


def reduce_and_get_magnitude(numbers: Input) -> int:
    while len(numbers) > 1:
        number = reduce([ OPEN ] + numbers[0] + numbers[1] + [ CLOSE ])
        numbers = [number] + (numbers[2:] if len(numbers) > 2 else [])
    return get_magnitude(numbers[0])


def part1(numbers: Input) -> int:
    return reduce_and_get_magnitude(numbers)


def part2(numbers: Input) -> int:
    maximum = 0
    for first in range(len(numbers)):
        for second in range(len(numbers)):
            if first == second:
                continue
            magnitude = reduce_and_get_magnitude([ numbers[first], numbers[second] ])
            maximum = magnitude if magnitude > maximum else maximum
    return maximum


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def encode_character(c: str) -> int:
    if c.isdigit():
        return int(c)
    if c == '[':
        return OPEN
    if c == ']':
        return CLOSE
    raise Exception(f"Unexpected character '{c}'")


def process_line(line: str):
    return [ encode_character(c) for c in line if c != ',' ]

def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ process_line(line.strip()) for line in file.readlines() ]


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
