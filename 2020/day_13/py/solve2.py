#! /usr/bin/python3

from typing import NamedTuple

from common import getInput, Bus


class BusPair():
    def __init__(self, first, second, offset, firstStart, secondStart):
        self.first = first
        self.second = second
        self.offset = offset
        self.firstStart = firstStart
        self.secondStart = secondStart
        self.previousStepTested = 0
        self.stepMultiplier = 1


    def __str__(self):
        return f"B {self.first} | B {self.second} / O {self.offset} / S {self.firstStart} | S {self.secondStart}"
    def __repr__(self):
        return self.__str__()


def buildPair(first, second):
    print("Building pair", first, second)
    offset = second.index - first.index
    multiplier = 1
    while True:
        a = (second.id * multiplier - offset) / first.id
        if a == int(a):
            return BusPair(first, second, offset, int(a), multiplier)
        multiplier += 1 


def main():
    timestamp, buses = getInput()
    pairs = []
    lastBus = buses[0]
    for bus in buses[1:]:
        if bus.isX:
            continue
        pairs.append(buildPair(lastBus, bus))
        lastBus = bus
    
    for pair in pairs:
        print(pair)
    step = 0
    firstPair = pairs[0]
    otherPairs = pairs[1:]

    while True:
        previousMultiplier = firstPair.secondStart + firstPair.first.id * step
        sequenceFailed = False
        input(f"step {step}: {previousMultiplier}")

        for pair in otherPairs:
            nextStep = pair.previousStepTested
            while True:
                currentMultiplier = pair.firstStart + pair.second.id * nextStep
                print("innerStep:", nextStep, "currentMultiplier:", currentMultiplier)
                if  currentMultiplier > previousMultiplier:
                    print("sequence failed")
                    sequenceFailed = True
                    break
                if currentMultiplier == previousMultiplier:
                    if firstPair.stepMultiplier == 1:
                        firstPair.stepMultiplier = pair.second.id
                        print("Setting step multiplier to:", pair.second.id)
                    pair.previousStepTested = nextStep
                    print("sequence continued - setting", nextStep, "to pair", pair)
                    break
                nextStep += 1
            
            if sequenceFailed:
                break
        if not sequenceFailed:
            break
        step += firstPair.stepMultiplier

    for bus in buses:
        print(bus)
    firstPair = pairs[0]
    print("Result:", firstPair.first.id * ( firstPair.firstStart + firstPair.second.id * step))
        

        
    


if __name__ == "__main__":
    main()
