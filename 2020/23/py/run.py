#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


class Node:
    def __init__(self, value: int):
        self.next = self
        self.value = value


def build_linked_list(cups: List[int]) -> Tuple[Node, List[Node]]:
    start = previous = last = Node(cups[0])
    values = [start] * len(cups)
    values[start.value - 1] = start
    for cup in cups[1:]:
        last = Node(cup)
        previous.next = last
        values[last.value - 1] = last
        previous = last
    last.next = start
    return start, values


def play_game(cups: List[int], moves: int) -> Node:
    start, values = build_linked_list(cups)
    max_value = max(cups)
    current = start
    while moves:
        moves -= 1
        first_removed = current.next
        last_removed = first_removed.next.next
        removed_values = {first_removed.value,
                          first_removed.next.value, last_removed.value}
        current.next = last_removed.next
        destination_value = current.value - 1
        while destination_value in removed_values or destination_value < 1:
            destination_value -= 1
            if destination_value < 0:
                destination_value = max_value

        destination_link = values[destination_value - 1]
        last_removed.next = destination_link.next
        destination_link.next = first_removed
        current = current.next
    return values[0]


def part1(cups: List[int]) -> str:
    one_node = play_game(cups, 100)
    result: List[int] = []
    current_node = one_node.next
    while current_node.value != 1:
        result.append(current_node.value)
        current_node = current_node.next
    return "".join(map(str, result))


def part2(cups: List[int]) -> int:
    cups += [*range(10, 10**6 + 1)]
    one_node = play_game(cups, 10**7)
    print(one_node.next.value, one_node.next.next.value)
    return one_node.next.value * one_node.next.next.value


def solve(cups: List[int]) -> Tuple[str, int]:
    return (
        part1(cups),
        part2(cups)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(c) for c in file.read().strip()]


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
