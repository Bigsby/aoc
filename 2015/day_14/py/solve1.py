#! /usr/bin/python3

from common import getInput


def calculateDistance(entry, totalDuration):
    period = entry.duration + entry.rest
    periods, remainder = divmod(totalDuration, period)
    total = periods * entry.speed * entry.duration
    remainderTotal = entry.speed if remainder >= entry.duration else entry.speed * (entry.duration - remainder)
    total += remainderTotal
    return total


def main():
    entries = list(getInput())
    for entry in entries:
        print(entry)
    totalDuration = 2503
    result = max(map(lambda entry: calculateDistance(entry, totalDuration), entries))
    print("Longest distance:", result)


if __name__ == "__main__":
    main()
