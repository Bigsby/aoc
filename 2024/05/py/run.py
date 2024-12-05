#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict

Rule = Tuple[int,int]
Input = Tuple[List[Rule],Dict[int,List[int]]]

def is_update_correct(update: List[int], rules: List[Rule]) -> bool:
    for index in range(1, len(update)):
        for previous_page in update[:index]:
            if update[index] in rules and previous_page in rules[update[index]]:
                return False
    return True


def part1(puzzle_input: Input) -> int:
    rules, updates = puzzle_input
    return sum(update[len(update) // 2] for update in updates if is_update_correct(update, rules))


def order_update_get_middle(update: List[int], rules: List[Rule]) -> int:
    ordered_update = []
    for page in update:
        insert_index = 0
        while insert_index < len(ordered_update):
            if page in rules and ordered_update[insert_index] in rules[page]:
                break
            insert_index += 1
        ordered_update.insert(insert_index, page)
    return ordered_update[len(update) // 2]


def part2(puzzle_input: Input) -> int:
    rules, updates = puzzle_input
    return sum(order_update_get_middle(update, rules) for update in updates if not is_update_correct(update, rules))


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        rules = dict() 
        updates = []
        reading_rules = True
        for line in file.readlines():
            line = line.strip()
            if not line:
                reading_rules = False
                continue
            if reading_rules:
                before, after = line.split("|")
                before = int(before)
                after = int(after)
                if before not in rules:
                    rules[before] = []
                rules[before].append(after)
            else:
                updates.append([int(page) for page in line.split(",")])

        return rules, updates


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
