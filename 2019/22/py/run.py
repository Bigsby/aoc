#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple

Shuffle = Tuple[int, int]
NEW_STACK, CUT, INCREMENT = 0, 1, 2


def do_shuffles(cards: List[int], shuffles: List[Shuffle]) -> List[int]:
    cards_count = len(cards)
    replacement = [0] * cards_count
    for shuffle, count in shuffles:
        if shuffle == NEW_STACK:
            cards = cards[::-1]
        elif shuffle == CUT:
            cards = cards[count:] + cards[:count]
        else:
            for index in range(cards_count):
                replacement[(index * count) % cards_count] = cards.pop(0)
            cards = replacement
    return cards


def inverse_modulo(a: int, n: int) -> int:
    return pow(a, n-2, n)


CARDS2 = 119315717514047
RUNS = 101741582076661
POSITION2 = 2020


def part2(shuffles: List[Shuffle]) -> int:
    la = lb = 0
    a, b = 1, 0
    for shuffle, count in shuffles:
        if shuffle == NEW_STACK:
            la, lb = -1, -1
        elif shuffle == INCREMENT:
            la, lb = count, 0
        else:
            la, lb = 1, -count
        a = (la * a) % CARDS2
        b = (la * b + lb) % CARDS2
    Ma = pow(a, RUNS, CARDS2)
    Mb = (b * (Ma - 1) * inverse_modulo(a - 1, CARDS2)) % CARDS2
    return ((POSITION2 - Mb) * inverse_modulo(Ma, CARDS2)) % CARDS2


CARDS1 = 10007
POSITION1 = 2019


def solve(shuffles: List[Shuffle]) -> Tuple[int, int]:
    return (
        do_shuffles([card for card in range(CARDS1)],
                    shuffles).index(POSITION1),
        part2(shuffles)
    )


def parse_line(line: str) -> Shuffle:
    if line.startswith("deal into"):
        return NEW_STACK, 0
    if line.startswith("cut"):
        return CUT, int(line.split(" ")[1])
    if line.startswith("deal with"):
        return INCREMENT, int(line.split(" ")[-1])
    raise Exception("Unknow shuffle", line)


def get_input(file_path: str):
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
