#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, List, Tuple
import re

Passport = Dict[str,str]
MANDATORY_FIELDS = [ 
    "byr", 
    "iyr", 
    "eyr", 
    "hgt", 
    "hcl", 
    "ecl", 
    "pid"
]


def countValidPassports(passports: List[Passport], validationFunc: Callable[[Passport], bool]) -> int:
    return sum(map(lambda passport: validationFunc(passport), passports))


def validateInt(value: str, min: int, max: int) -> bool:
    try:
        parsed = int(value)
        return parsed >= min and parsed <= max
    except:
        return False


hgtRegEx = re.compile(r"^(\d{2,3})(cm|in)$")
def validateHgt(value: str) -> bool:
    match = hgtRegEx.match(value)
    if match:
        height = int(match.group(1))
        if match.group(2) == "cm":
            return height >= 150 and height <= 193
        else:
            return height >= 59 and height <= 76
    return False


hclRegex = re.compile(r"^#[0-9a-f]{6}$")
ECLS = [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]
pidRegex = re.compile(r"^[\d]{9}$")
VALIDATIONS: Dict[str,Callable[[str],bool]] = {
    "byr": lambda value: validateInt(value, 1920, 2002),
    "iyr": lambda value: validateInt(value, 2010, 2020),
    "eyr": lambda value: validateInt(value, 2020, 2030),
    "hgt": validateHgt,
    "hcl": lambda value: hclRegex.match(value),
    "ecl": lambda value: value in ECLS,
    "pid": lambda value: pidRegex.match(value)
}
def solve(passports: List[Passport]) -> Tuple[int,int]:
    return (
        countValidPassports(passports, lambda passport: 
            all(map(lambda field: field in passport, MANDATORY_FIELDS))),
        countValidPassports(passports, 
            lambda passport: all(map(lambda field: 
                field in passport and VALIDATIONS[field](passport[field]), MANDATORY_FIELDS)))
    )


entryRegEx = re.compile(r"([a-z]{3})\:([^\s]+)")
def getInput(filePath: str) -> List[Passport]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath) as file:
        return [ dict(entryRegEx.findall(entry)) for entry in file.read().split("\n\n") ]


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