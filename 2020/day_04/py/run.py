#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


def countValidPassports(passports, validationFunc):
    return reduce(lambda currentCount, passport: currentCount + validationFunc(passport), passports, 0)
    

passportMandatoryFields = [ 
    'byr', 
    'iyr', 
    'eyr', 
    'hgt', 
    'hcl', 
    'ecl', 
    'pid'
]
def isPassportValid(passport):
    for field in passportMandatoryFields:
        if not (field in passport):
            return False
    return True


def part1(puzzleInput):
    return countValidPassports(puzzleInput, isPassportValid)


def validate_int(value, min, max):
    try:
        parsed = int(value)
        return parsed >= min and parsed <= max
    except:
        return False


hgtRegEx = re.compile('^(\d{2,3})(cm|in)$')
def validate_hgt(value):
    match = hgtRegEx.match(value)
    if match:
        height = int(match.group(1))
        if match.group(2) == "cm":
            return height >= 150 and height <= 193
        else:
            return height >= 59 and height <= 76
    return False


hclRegEx = re.compile('^#[0-9a-f]{6}$')
ecls = [ "amb", "blu", "brn", "gry", "grn", "hzl", "oth" ]
pidRegEx = re.compile("^[\d]{9}$")
validations = {
    'byr': lambda value: validate_int(value, 1920, 2002),
    'iyr': lambda value: validate_int(value, 2010, 2020),
    'eyr': lambda value: validate_int(value, 2020, 2030),
    'hgt': validate_hgt,
    'hcl': lambda value: hclRegEx.match(value),
    'ecl': lambda value: value in ecls,
    'pid': lambda value: pidRegEx.match(value)
}
def isPassportValid2(passport):
    for field in passportMandatoryFields:
        if not (field in passport) or not validations[field](passport[field]):            
            return False
    return True


def part2(puzzleInput):
    return countValidPassports(puzzleInput, isPassportValid2)


entryRegEx = re.compile('([a-z]{3})\:([^\s]+)')
def getInput(filePath):
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