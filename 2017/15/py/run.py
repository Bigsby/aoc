#! /usr/bin/python3

import sys
import os
import time
from typing import Generator, Tuple
import re


MODULUS = 2147483647


def build_generator(number: int, factor: int, divisor: int) -> Generator[int, int, int]:
    while True:
        number = number * factor % MODULUS
        if number % divisor == 0:
            yield number & 0xffff


FACTOR_A = 16807
FACTOR_B = 48271


def run_sequences(generators: Tuple[int, int], divisor_a: int, divisor_b: int, million_cycles: int) -> int:
    generator_a, generator_b = generators
    sequence_a, sequence_b = build_generator(
        generator_a, FACTOR_A, divisor_a), build_generator(generator_b, FACTOR_B, divisor_b)
    return sum(next(sequence_a) == next(sequence_b) for _ in range(million_cycles * (10 ** 6)))


DIVISOR_A = 4
DIVISOR_B = 8


def solve(generators: Tuple[int, int]) -> Tuple[int, int]:
    return (
        run_sequences(generators, 1, 1, 40),
        run_sequences(generators, DIVISOR_A, DIVISOR_B, 5)
    )


numbers_regex = re.compile(r"\d+")


def get_input(file_path: str) -> Tuple[int, int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        matches = numbers_regex.findall(file.read())
        return int(matches[0]), int(matches[1])


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
