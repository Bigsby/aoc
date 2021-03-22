#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re


class Replacement():
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target

    def __str__(self) -> str:
        return f"{self.source} => {self.target}"


def processReplacement(molecule: str, replacement: Replacement) -> List[str]:
    return ["".join([molecule[:match.start()], replacement.target, molecule[match.end():]]) for match in re.finditer(replacement.source, molecule)]


def part1(puzzleInput: Tuple[List[Replacement], str]) -> int:
    replacements, molecule = puzzleInput
    newMolecules: List[str] = []
    for replacement in replacements:
        for newMolecule in processReplacement(molecule, replacement):
            newMolecules.append(newMolecule)

    return len(set(newMolecules))


def part2(puzzleInput: Tuple[List[Replacement], str]) -> int:
    replacements, molecule = puzzleInput
    targetMolecule = "e"
    molecule = molecule[::-1]
    repDict = {rep.target[::-1]: rep.source[::-1] for rep in replacements}
    count = 0
    while molecule != targetMolecule:
        molecule = re.sub("|".join(repDict.keys()),
                          lambda match: repDict[match.group()], molecule, 1)
        count += 1
    return count


def solve(puzzleInput: Tuple[List[Replacement], str]) -> Tuple[int, int]:
    return (
        part1(puzzleInput),
        part2(puzzleInput)
    )


lineRegex = re.compile(r"^(\w+)\s=>\s(\w+)$")


def getInput(filePath: str) -> Tuple[List[Replacement], str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        replacements: List[Replacement] = []
        molecule = ""
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                replacements.append(Replacement(*match.group(1, 2)))
            else:
                molecule += line
        return replacements, molecule.strip()


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
