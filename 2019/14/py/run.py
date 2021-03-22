#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re
from collections import defaultdict
import math

ChemicalPortion = Tuple[int, str]


def calculate_required_ore(reactions: Dict[str, Tuple[int, List[ChemicalPortion]]], required_fuel: int) -> int:
    required_chemicals = defaultdict(int, {'FUEL': required_fuel})
    produced_chemicals: Dict[str, int] = defaultdict(int)
    ore_count = 0
    while required_chemicals:
        item, amount = required_chemicals.popitem()
        if amount <= produced_chemicals[item]:
            produced_chemicals[item] -= amount
            continue
        amount_needed = amount - produced_chemicals[item]
        del produced_chemicals[item]
        amount_produced, portions = reactions[item]
        required_quantity = math.ceil(amount_needed / amount_produced)
        produced_chemicals[item] += (required_quantity *
                                     amount_produced) - amount_needed
        for other_amount_required, chemical in portions:
            chemical_value = other_amount_required * required_quantity
            if chemical == "ORE":
                ore_count += chemical_value
            else:
                required_chemicals[chemical] += chemical_value
    return ore_count


def part2(reactions: Dict[str, Tuple[int, List[ChemicalPortion]]]):
    required_fuel = 1
    last_needed = calculate_required_ore(reactions, required_fuel)
    max_ore = 10 ** 12
    while True:
        required_fuel = required_fuel * max_ore // last_needed
        ore_needed = calculate_required_ore(reactions, required_fuel)
        if last_needed == ore_needed:
            break
        else:
            last_needed = ore_needed
    return required_fuel


def solve(reactions: Dict[str, Tuple[int, List[ChemicalPortion]]]) -> Tuple[int, int]:
    return (
        calculate_required_ore(reactions, 1),
        part2(reactions)
    )


line_regex = re.compile(r"(\d+)\s([A-Z]+)")


def parse_line(line: str) -> Tuple[str, int, List[ChemicalPortion]]:
    matches = line_regex.findall(line)
    result = matches.pop()
    return result[1], int(result[0]), [(int(part[0]), part[1]) for part in matches]


def get_input(file_path: str) -> Dict[str, Tuple[int, List[ChemicalPortion]]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return {chemical: (amount, reactions)
                for chemical, amount, reactions in [parse_line(line) for line in file.readlines()]}


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
