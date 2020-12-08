#! /usr/bin/python3

from common import getInput


def isValidRecord(reading, record):
    for prop in reading:
        recordValue = record.props[prop]
        if recordValue == "N/A":
            continue
        if recordValue != reading[prop]:
            return False
    return True


def main():
    auntRecords = list(getInput())
    mfcsamReading = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 5,
        "cars": 2,
        "perfumes": 1
    }

    for record in auntRecords:
        if isValidRecord(mfcsamReading, record):
            print("Aunt is number:", record.number)


if __name__ == "__main__":
    main()
