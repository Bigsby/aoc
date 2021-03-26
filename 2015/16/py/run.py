#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re
from enum import Enum


class AuntRecord():
    def __init__(self, number: str, prop1_name: str, prop1_value: str, prop2_name: str, prop2_value: str, prop3_name: str, prop3_value: str):
        self.number = int(number)
        self.props = AuntRecord.build_prop_dict()
        self.set_prop(prop1_name, prop1_value)
        self.set_prop(prop2_name, prop2_value)
        self.set_prop(prop3_name, prop3_value)

    def set_prop(self, name: str, value: str):
        self.props[name] = int(value)

    @staticmethod
    def build_prop_dict() -> Dict[str, int]:
        return {prop: AuntRecord.NA_PROP for prop in AuntRecord.PROPS}

    PROPS = ["children", "cats", "samoyeds", "pomeranians",
             "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes"]
    NA_PROP = -1


class Operator(Enum):
    EQUAL = 0,
    GREATER = 1,
    LESS = 2


class Reading():
    def __init__(self, value: int, operator: Operator = Operator.EQUAL):
        self.value = value
        self.operator = operator


MFCSAN_READING: Dict[str, Reading] = {
    "children": Reading(3),
    "cats": Reading(7, Operator.GREATER),
    "samoyeds": Reading(2),
    "pomeranians": Reading(3, Operator.LESS),
    "akitas": Reading(0),
    "vizslas": Reading(0),
    "goldfish": Reading(5, Operator.LESS),
    "trees": Reading(3, Operator.GREATER),
    "cars": Reading(2),
    "perfumes": Reading(1)
}


def is_valid_record(record: AuntRecord, check_operator: bool = False) -> bool:
    for prop in MFCSAN_READING:
        record_value = record.props[prop]
        if record_value == AuntRecord.NA_PROP:
            continue
        reading = MFCSAN_READING[prop]
        reading_value = reading.value
        if check_operator:
            if reading.operator == Operator.EQUAL and record_value != reading_value \
                    or reading.operator == Operator.GREATER and record_value <= reading_value \
                    or reading.operator == Operator.LESS and record_value >= reading_value:
                return False
        elif record_value != reading_value:
            return False
    return True


def solve(aunts: List[AuntRecord]) -> Tuple[int, int]:
    return (
        next(filter(lambda record: is_valid_record(record), aunts)).number,
        next(filter(lambda record: is_valid_record(record, True), aunts)).number
    )


line_regex = re.compile(
    r"^Sue\s(\d+):\s(\w+):\s(\d+),\s(\w+):\s(\d+),\s(\w+):\s(\d+)$")


def parse_line(line: str):
    match = line_regex.match(line)
    if match:
        return AuntRecord(*match.group(1, 2, 3, 4, 5, 6, 7))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[AuntRecord]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


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
