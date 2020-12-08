#! /usr/bin/python3

from enum import Enum

from common import getInput


def isValidRecord(readings, record):
    print("testing", record)
    for prop in readings:
        recordValue = record.props[prop]
        if recordValue == "N/A":
            continue
        reading = readings[prop]
        readingValue = reading.value
        if reading.operator == Operator.EQUAL and recordValue != readingValue:
            return False
        if reading.operator == Operator.GREATER and recordValue <= readingValue:
            return False
        if reading.operator == Operator.LESS and recordValue >= readingValue:
            return False
    return True


class Operator(Enum):
    EQUAL = 0,
    GREATER = 1,
    LESS = 2

class Reading():
    def __init__(self, value, operator = Operator.EQUAL):
        self.value = value
        self.operator = operator


def main():
    auntRecords = list(getInput())
    mfcsamReading = {
        "children": Reading(3),
        "cats": Reading(7, Operator.GREATER),
        "samoyeds": Reading(2),
        "pomeranians": Reading(3, Operator.LESS),
        "akitas": Reading(0),
        "vizslas": Reading(0),
        "goldfish": Reading(5, Operator.LESS),
        "trees": Reading(5, Operator.GREATER),
        "cars": Reading(2),
        "perfumes": Reading(1)
    }

    for record in auntRecords:
        if isValidRecord(mfcsamReading, record):
            print("Aunt is number:", record.number)
            break


if __name__ == "__main__":
    main()
