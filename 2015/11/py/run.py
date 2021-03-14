#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple
import re


FORBIDDEN_LETTERS = [ord("i"), ord("o"), ord("l")]
pairs_regex = re.compile(r"^.*(.)\1{1}.*(.)\2{1}.*$")


def is_password_valid(password: str) -> bool:
    if not pairs_regex.match(password):
        return False
    ords = list(map(lambda c: ord(c), password))
    for index in range(len(ords) - 2):
        if ords[index] == ords[index + 1] - 1 and ords[index] == ords[index + 2] - 2:
            return True
    return False


def get_next_char(c: int) -> str:
    c += 1
    while c in FORBIDDEN_LETTERS:
        c += 1
    return chr(c)


A_CHR = "a"
Z_ORD = ord("z")


def calculate_next_password(current_password: str) -> str:
    result = list(current_password)
    for index in range(len(result) - 1, 0, -1):
        c_ord = ord(result[index])
        if c_ord == Z_ORD:
            result[index] = A_CHR
            continue
        result[index] = get_next_char(c_ord)
        break
    return "".join(result)


def calculate_next_valid_password(current_password: str) -> str:
    current_password = calculate_next_password(current_password)
    while not is_password_valid(current_password):
        current_password = calculate_next_password(current_password)
    return current_password


def solve(current_password: str) -> Tuple[str, str]:
    part1 = calculate_next_valid_password(current_password)
    return (part1, calculate_next_valid_password(part1))


def get_input(file_path: str):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read().strip()


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2R_rsult = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2R_rsult)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
