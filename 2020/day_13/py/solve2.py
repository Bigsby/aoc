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
    

    for index in range(len(pairs) - 1):
        currentPair = pairs[index]
        currentJump = currentPair.first.id
        currentStep = currentPair.previousStepTested

        nextPair = pairs[index + 1]
        nextJump = nextPair.second.id
        nextStep = nextPair.previousStepTested

        lastMultiplier = 1

        while True:            
            currentMultiplier = currentPair.secondStart + currentStep * currentJump
            
            isEqual = False

            while True:
                nextMultiplier = nextPair.firstStart + nextStep * nextJump
                if nextMultiplier > currentMultiplier:
                    break
                if nextMultiplier == currentMultiplier:
                    nextPair.previousStepTested = nextStep
                    nextPair.stepMultiplier = currentPair.stepMultiplier * currentPair.first.id
                    lastMultiplier = nextMultiplier
                    isEqual = True
                    break
                nextStep += 1

            if isEqual:
                break
            currentStep += currentPair.stepMultiplier


    lastPair = pairs[len(pairs)-1]
    offset = lastPair.first.index
    result = lastPair.first.id * lastMultiplier - offset
    print("Result:", result)



if __name__ == "__main__":
    main()
