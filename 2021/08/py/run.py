#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict

Connection = Tuple[List[str], List[str]]


def part1(connections: List[Connection]) -> int:
    total = 0
    for connection in connections:
        total += sum([ 1 for wire in connection[1] if len(wire) in [2, 3, 4, 7]])
    return total 


def len_of_except(target: str, known: str) -> int:
    return len([ segment for segment in target if segment not in known])


def filter_and_remove(wires: List[str], digits: List[str], digit: int, digit_length: int, except_digit: int, except_length: int):
    digits[digit] = list(filter(
        lambda wire: len(wire) == digit_length and (except_length == 0 or len_of_except(wire, digits[except_digit]) == except_length), wires))[0]
    wires.remove(digits[digit])


def get_connection_number(connection: Connection):
    wires, displays = connection
    wires = list(map(lambda wire: "".join((sorted(list(wire)))), wires))
    displays = list(map(lambda display: "".join((sorted(list(display)))), displays))
    digits = [ "" ] * 10
    filter_and_remove(wires, digits, 7, 3, 0, 0)
    filter_and_remove(wires, digits, 4, 4, 0, 0)
    filter_and_remove(wires, digits, 1, 2, 0, 0)
    filter_and_remove(wires, digits, 8, 7, 0, 0)
    filter_and_remove(wires, digits, 3, 5, 1, 3)
    filter_and_remove(wires, digits, 6, 6, 1, 5)
    filter_and_remove(wires, digits, 2, 5, 4, 3)
    filter_and_remove(wires, digits, 5, 5, 4, 2)
    filter_and_remove(wires, digits, 0, 6, 4, 3)
    digits[9] = wires[0]
    decode = dict([ (digits[index], index) for index in range(10) ])
    total = 0
    for index, display in enumerate(displays):
        total += decode[display] * (10 ** (3 - index))
    return total


def part2(connections: List[Connection]) -> int:
    total = 0
    for connection in connections:
        total += get_connection_number(connection)
    return total


def solve(connections: List[Connection]) -> Tuple[int,int]:
    return (part1(connections), part2(connections))


def parseLine(line: str) -> Connection:
    wires, displays = tuple(line.split(" | "))
    return (
        [ wire.strip() for wire in wires.split(" ") ],
        [ display.strip() for display in displays.split(" ") ]
    )


def get_input(file_path: str) -> List[Connection]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ parseLine(line) for line in file.readlines() ]


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
