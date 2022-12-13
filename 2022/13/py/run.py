#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Union, List, cast
from functools import cmp_to_key

Input = List[object]


def are_in_order(left: object, right: object) -> Union[bool, None]:
    if type(left) != type(right):
        if type(left) == int:
            return are_in_order([left], right)
        else:
            return are_in_order(left, [right])
    if type(left) == int:
        if left == right:
            return
        return int(str(left)) < int(str(right))
    left_list: List[object] = cast(List[object], left)
    right_list: List[object] = cast(List[object], right)
    for inner_left, inner_right in zip(left_list, right_list):
        inner_in_order = are_in_order(inner_left, inner_right)
        if inner_in_order is not None:
            return inner_in_order
    if len(left_list) != len(right_list):
        return len(left_list) < len(right_list)


def part1(packets: Input) -> int:
    ordered_sum = 0
    for pair in range(len(packets) // 2):
        left, right = packets[pair * 2], packets[pair * 2 + 1]
        if are_in_order(left, right):
            ordered_sum += pair + 1
    return ordered_sum


def part2(packets: Input) -> int:
    divider_1 = [[2]]
    divider_2 = [[6]]
    packets.append(divider_1)
    packets.append(divider_2)
    packets.sort(key=cmp_to_key(lambda left, right: -1 if are_in_order(left, right) else 1))
    decoder_key = 1
    for index, packet in enumerate(packets):
        if packet == divider_1 or packet == divider_2:
            decoder_key *= index + 1
    return decoder_key


def solve(puzzle_input: Input) -> Tuple[int, int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [eval(line.strip()) for line in file.readlines() if line.strip()]


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
