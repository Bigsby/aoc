#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, List
import re

Passport = Dict[str,str]


def countValidPassports(passports: List[Passport], validationFunc: Callable[[Passport], bool]) -> int:
    return sum(map(lambda passport: validationFunc(passport), passports))
    

MANDATORY_FIELDS = [ 
    'byr', 
    'iyr', 
    'eyr', 
    'hgt', 
    'hcl', 
    'ecl', 
    'pid'
]
def isPassportValid(passport: Passport) -> bool:
    for field in MANDATORY_FIELDS:
        if not (field in passport):
            return False
    return True


def part1(puzzleInput: List[Passport]) -> int:
    return countValidPassports(puzzleInput, isPassportValid)


def validate_int(value: str, min: int, max: int) -> bool:
    try:
        parsed = int(value)
        return parsed >= min and parsed <= max
    except:
        return False


hgtRegEx = re.compile(r"^(\d{2,3})(cm|in)$")
def validate_hgt(value: str) -> bool:
    match = hgtRegEx.match(value)
    if match:
        height = int(match.group(1))
        if match.group(2) == "cm":
            return height >= 150 and height <= 193
        else:
            return height >= 59 and height <= 76
    return False


hclRegEx = re.compile(r"^#[0-9a-f]{6}$")
ecls = [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]
pidRegEx = re.compile(r"^[\d]{9}$")
VALIDATIONS: Dict[str,Callable[[str],bool]] = {
    'byr': lambda value: validate_int(value, 1920, 2002),
    'iyr': lambda value: validate_int(value, 2010, 2020),
    'eyr': lambda value: validate_int(value, 2020, 2030),
    'hgt': validate_hgt,
    'hcl': lambda value: hclRegEx.match(value),
    'ecl': lambda value: value in ecls,
    'pid': lambda value: pidRegEx.match(value)
}
def isPassportValid2(passport: Passport) -> bool:
    for field in MANDATORY_FIELDS:
        if not (field in passport) or not VALIDATIONS[field](passport[field]):            
            return False
    return True


def part2(puzzleInput: List[Dict[str,str]]) -> int:
    return countValidPassports(puzzleInput, isPassportValid2)


entryRegEx = re.compile(r"([a-z]{3})\:([^\s]+)")
def getInput(filePath: str) -> List[Passport]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath) as file:
        return [ dict(entryRegEx.findall(entry)) for entry in file.read().split("\n\n") ]


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