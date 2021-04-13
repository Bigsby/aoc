#! /usr/bin/python3

import sys
import os
import time
from typing import Deque, List, Tuple
from collections import deque

Instruction = Tuple[int, int, int]
SWAP_POSITION = 0
SWAP_LETTER = 1
ROTATE_LEFT = 2
ROTATE_RIGHT = 3
ROTATE_LETTER = 4
REVERSE = 5
MOVE = 6


def process(start: str, instructions: List[Instruction], reverse: bool = False) -> str:
    password: Deque[int] = deque(ord(value) for value in start)
    if reverse:
        instructions.reverse()
    for op_code, a, b in instructions:
        if op_code == SWAP_POSITION:
            old_a = password[a]
            password[a] = password[b]
            password[b] = old_a
        elif op_code == SWAP_LETTER:
            index_of_a = password.index(a)
            index_of_b = password.index(b)
            old_a = password[index_of_a]
            password[index_of_a] = password[index_of_b]
            password[index_of_b] = old_a
        elif op_code == ROTATE_LEFT:
            password.rotate(a if reverse else -a)
        elif op_code == ROTATE_RIGHT:
            password.rotate(-a if reverse else a)
        elif op_code == ROTATE_LETTER:
            index_of_a = password.index(a)
            rotation = index_of_a + 1 + (1 if index_of_a >= 4 else 0)
            if reverse:
                rotation = -(index_of_a // 2 + (1 if index_of_a %
                             2 == 1 or index_of_a == 0 else 5))
            password.rotate(rotation)
        elif op_code == REVERSE:
            password_list = list(password)
            password = deque(
                password_list[:a] + password_list[a:b + 1][::-1] + password_list[b + 1:])
        elif op_code == MOVE:
            origin, destination = (b, a) if reverse else (a, b)
            letter_to_move = password[origin]
            password.remove(letter_to_move)
            password.insert(destination, letter_to_move)
    return "".join(chr(c) for c in password)


def solve(instructions: List[Instruction]) -> Tuple[str, str]:
    return (
        process("abcdefgh", instructions),
        process("fbgdceah", instructions, True)
    )


def parse_line(line: str) -> Instruction:
    if line.startswith("swap position"):
        return (SWAP_POSITION, int(line[14]), int(line[-1]))
    elif line.startswith("swap letter"):
        return (SWAP_LETTER, ord(line[12]), ord(line[-1]))
    elif line.startswith("rotate left"):
        return (ROTATE_LEFT, int(line[12]), 0)
    elif line.startswith("rotate right"):
        return (ROTATE_RIGHT, int(line[13]), 0)
    elif line.startswith("rotate based"):
        return (ROTATE_LETTER, ord(line[-1]), 0)
    elif line.startswith("reverse"):
        return (REVERSE, int(line[18]), int(line[-1]))
    elif line.startswith("move"):
        return (MOVE, int(line[14]), int(line[-1]))
    raise Exception("Unknow instruction", line)


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line.strip()) for line in file.readlines()]


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
