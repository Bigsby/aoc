#! /usr/bin/python3

import sys, os, time
from typing import Callable, Dict, List, Tuple
import re

Passport = Dict[str, str]
MANDATORY_FIELDS = [
    "byr",
    "iyr",
    "eyr",
    "hgt",
    "hcl",
    "ecl",
    "pid"
]


def count_valid_passports(passports: List[Passport], validation_func: Callable[[Passport], bool]) -> int:
    return sum(map(lambda passport: validation_func(passport), passports))


def validate_int(value: str, min: int, max: int) -> bool:
    try:
        parsed = int(value)
        return parsed >= min and parsed <= max
    except:
        return False


hgt_regex = re.compile(r"^(\d{2,3})(cm|in)$")
def validate_hgt(value: str) -> bool:
    match = hgt_regex.match(value)
    if match:
        height = int(match.group(1))
        if match.group(2) == "cm":
            return height >= 150 and height <= 193
        else:
            return height >= 59 and height <= 76
    return False


hcl_regex = re.compile(r"^#[0-9a-f]{6}$")
ECLS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
pid_regex = re.compile(r"^[\d]{9}$")
VALIDATIONS: Dict[str, Callable[[str], bool]] = {
    "byr": lambda value: validate_int(value, 1920, 2002),
    "iyr": lambda value: validate_int(value, 2010, 2020),
    "eyr": lambda value: validate_int(value, 2020, 2030),
    "hgt": validate_hgt,
    "hcl": lambda value: hcl_regex.match(value),
    "ecl": lambda value: value in ECLS,
    "pid": lambda value: pid_regex.match(value)
}
def solve(passports: List[Passport]) -> Tuple[int, int]:
    return (
        count_valid_passports(passports, lambda passport:
                              all(map(lambda field: field in passport, MANDATORY_FIELDS))),
        count_valid_passports(passports, lambda passport:
                              all(map(lambda field:
                                      field in passport and VALIDATIONS[field](passport[field]), MANDATORY_FIELDS)))
    )


entry_regex = re.compile(r"([a-z]{3})\:([^\s]+)")
def get_input(file_path: str) -> List[Passport]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        return [dict(entry_regex.findall(entry)) for entry in file.read().split("\n\n")]


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
