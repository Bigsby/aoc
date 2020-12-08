#! /usr/bin/python3

from common import getInput

def getDistanceForTime(entry, time):
    timeInPeriod = time % entry.period
    return entry.speed if timeInPeriod < entry.duration else 0

    

def main():
    entries = list(getInput())
    totalTime = 2503
    deers = { entry.name: { "distance": 0, "points": 0, "entry": entry } for entry in entries }

    for time in range(0, totalTime):
        maxDistance = 0
        for name in deers:
            deer = deers[name]
            deer["distance"] += getDistanceForTime(deer["entry"], time)
            maxDistance = max(maxDistance, deer["distance"])
        for name in deers:
            if deers[name]["distance"] == maxDistance:
                deers[name]["points"] += 1

    result = max(map(lambda name: deers[name]["points"], deers.keys()))
    print("Most points:", result)


if __name__ == "__main__":
    main()
