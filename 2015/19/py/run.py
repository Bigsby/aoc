#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from dataclasses import dataclass
import re


@dataclass
class Replacement():
    source: str
    target: str


def process_replacement(molecule: str, replacement: Replacement) -> List[str]:
    return ["".join([molecule[:match.start()], replacement.target, molecule[match.end():]])
            for match in re.finditer(replacement.source, molecule)]


def part1(puzzle_input: Tuple[List[Replacement], str]) -> int:
    replacements, molecule = puzzle_input
    new_molecules: List[str] = []
    for replacement in replacements:
        for new_molecule in process_replacement(molecule, replacement):
            new_molecules.append(new_molecule)
    return len(set(new_molecules))


def part2(puzzle_input: Tuple[List[Replacement], str]) -> int:
    replacements, molecule = puzzle_input
    target_molecule = "e"
    molecule = molecule[::-1]
    replacement_dictionary = {
        rep.target[::-1]: rep.source[::-1] for rep in replacements}
    count = 0
    replacements_regex = re.compile("|".join(replacement_dictionary.keys()))
    while molecule != target_molecule:
        molecule = replacements_regex.sub(
            lambda match: replacement_dictionary[match.group()], molecule, 1)
        count += 1
    return count


def solve(puzzle_input: Tuple[List[Replacement], str]) -> Tuple[int, int]:
    return (
        part1(puzzle_input),
        part2(puzzle_input)
    )


line_regex = re.compile(r"^(\w+)\s=>\s(\w+)$")


def get_input(file_path: str) -> Tuple[List[Replacement], str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        replacements: List[Replacement] = []
        molecule = ""
        for line in file.readlines():
            match = line_regex.match(line)
            if match:
                replacements.append(Replacement(*match.group(1, 2)))
            else:
                molecule += line
        return replacements, molecule.strip()


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
