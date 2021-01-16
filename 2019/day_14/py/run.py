#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re
from collections import defaultdict
import math

ChemicalPortion = Tuple[int,str]


def getRequiredOre(reactions: Dict[str,Tuple[int,List[ChemicalPortion]]], requireFuel: int) -> int:
    requiredChemicals = defaultdict(int, {'FUEL': requireFuel})
    producedChemicals: Dict[str,int] = defaultdict(int)
    oreCount = 0
    while requiredChemicals:
        item, amount = requiredChemicals.popitem()
        if amount <= producedChemicals[item]:
            producedChemicals[item] -= amount
            continue

        amountNeeded = amount - producedChemicals[item]
        del producedChemicals[item]
        amountProduced, portions = reactions[item]
        requiredQuantity = math.ceil(amountNeeded / amountProduced)

        producedChemicals[item] += (requiredQuantity * amountProduced) - amountNeeded
        for otherAmountRequired, chemical in portions:
            chemicalValue = otherAmountRequired * requiredQuantity
            if chemical == "ORE":
                oreCount += chemicalValue
            else:
                requiredChemicals[chemical] += chemicalValue

    return oreCount


def part1(reactions: Dict[str,Tuple[int,List[ChemicalPortion]]]) -> int:
    return getRequiredOre(reactions, 1)


def part2(reactions: Dict[str,Tuple[int,List[ChemicalPortion]]]):
    requiredFuel = 1
    lastNeeded = getRequiredOre(reactions, requiredFuel)
    maxOre = 10 ** 12
    while True:
        requiredFuel = requiredFuel * maxOre // lastNeeded
        oreNeeded = getRequiredOre(reactions, requiredFuel)
        if lastNeeded == oreNeeded:
            break
        else:
            lastNeeded = oreNeeded
    return requiredFuel


lineRegex = re.compile(r"(\d+)\s([A-Z]+)")
def parseLine(line: str) -> Tuple[str,int,List[ChemicalPortion]]:
    matches = lineRegex.findall(line)
    result = matches.pop()
    return result[1], int(result[0]), [ (int(part[0]), part[1]) for part in matches ]

    
def getInput(filePath: str) -> Dict[str,Tuple[int,List[ChemicalPortion]]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return { chemical: (amount, reactions) for chemical, amount, reactions in  [ parseLine(line) for line in file.readlines() ] }


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()