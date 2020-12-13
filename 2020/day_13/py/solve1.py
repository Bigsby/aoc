#! /usr/bin/python3

import sys

from common import getInput

def main():
    timestamp, buses = getInput()
    print(timestamp)
    closestAfter = sys.maxsize
    closestBus = None
    for bus in buses:
        if not bus.isX:
            timeAfter = (int(timestamp / bus.id) + 1) * bus.id - timestamp
            if timeAfter < closestAfter:
                closestAfter = timeAfter
                closestBus = bus

    print("Closest bus:", bus)
    result = closestAfter * closestBus.id
    print("Result:", result)



if __name__ == "__main__":
    main()
