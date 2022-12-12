#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Callable
from copy import deepcopy


class Monkey():
    def __init__(self, items: List[int], operation: Callable[[int], int], test: int, throw_true: int, throw_false: int):
        self.items = items
        self.operation = operation
        self.test = test
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.inspections = 0


Input = List[Monkey]


def do_rounds(monkeys: Input, worry_level: int, rounds: int, common_divider: int) -> int:
    monkeys = deepcopy(monkeys)
    divide = common_divider != 1
    for _ in range(rounds):
        for monkey in monkeys:
            for item in monkey.items:
                item = monkey.operation(item) // worry_level
                if divide:
                    item %= common_divider
                monkeys[monkey.throw_true if (
                    item % monkey.test) == 0 else monkey.throw_false].items.append(item)
                monkey.inspections += 1
            monkey.items.clear()
    inspections = sorted(
        map(lambda monkey: monkey.inspections, monkeys), reverse=True)
    return inspections[0] * inspections[1]


def solve(monkeys: Input) -> Tuple[int, int]:
    common_divider = 1
    for monkey in monkeys:
        common_divider *= monkey.test
    return (do_rounds(monkeys, 3, 20, 1), do_rounds(monkeys, 1, 10_000, common_divider))


def process_operation(operation: str, operand: str) -> Callable[[int], int]:
    if operation == "*":
        if operand == "old":
            return lambda x: x * x
        else:
            value = int(operand)
            return lambda x: x * value
    else:
        if operand == "old":
            return lambda x: x + x
        else:
            value = int(operand)
            return lambda x: x + value


def process_input_monkey(input: str) -> Monkey:
    lines = [line.strip() for line in input.split("\n")]
    items_split = lines[1].split(": ")[1].strip().split(", ")
    operation_split = lines[2].split(" ")
    test_split = lines[3].split(" ")
    true_split = lines[4].split(" ")
    false_split = lines[5].split(" ")
    return Monkey(
        [int(item) for item in items_split],
        process_operation(operation_split[4], operation_split[5]),
        int(test_split[3]),
        int(true_split[5]),
        int(false_split[5])
    )


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [process_input_monkey(monkey_input) for monkey_input in file.read().split("\n\n")]


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
