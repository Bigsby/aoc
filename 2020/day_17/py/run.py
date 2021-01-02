#! /usr/bin/python3

import sys, os, time
from itertools import product

class Dimension(list):
    def __init__(self, upperLayer, outerDimension = False):
        self.offset = 0
        self.upperLayer = upperLayer
        if self.upperLayer is not None:
            self.upperLayer.append(self)
        self.outerDimension = outerDimension

    def __getitem__(self, key):
        return list.__getitem__(self, key + self.offset)
    def __setitem__(self, key, item):
        list.__setitem__(self, key + self.offset, item)

    def append(self, item):
        super().append(item)
        self.offset = len(self) // 2

    def getLimit(self):
        if len(self) % 2:
            return -self.offset, self.offset
        return -self.offset, self.offset - 1

    def copyGrow(self, upperLayer):
        result = Dimension(upperLayer)
        if isinstance(self[0], self.__class__):
            self[0].copyGrow(result)
            for item in self:
                item.copyGrow(result)
            self[0].copyGrow(result)
        else:     
            result.append(False)
            result.append(False)
            for item in self:
                result.append(False)

    def _indexedlayers(self):
        return [ (index, layer) for index, layer in enumerate(self) ]

    def __str__(self):
        if len(self):
            if self.outerDimension:
                return "".join(map(lambda indexedLayer: "".join(f"z={indexedLayer[0] - self.offset}\n{indexedLayer[1]}\n"), self._indexedlayers()))
            elif len(self) and isinstance(self[0], self.__class__):
                return "\n".join(map(lambda subLayer: str(subLayer), self))
            else:
                return "".join(map(lambda item: "#" if item else ".", self))
        else:
            return list.__str__(self)


class Universe(Dimension):
    def __init__(_):
        super().__init__(None, True)

    def isPositionValid(self, position):
        currentDimension = self
        for coordinate in position:
            bottom, top = currentDimension.getLimit()
            if coordinate < bottom or coordinate > top:
                return False
            if len(currentDimension) == 0:
                return False
            currentDimension = currentDimension[0]
        return True
    
    def addDimension(self):
        newDimension = Dimension(None, False)
        for innerDimension in self:
            newDimension.append(innerDimension)
            innerDimension.upperLayer = newDimension
        self.clear()
        self.append(newDimension)


    def getNeighbors(_, position):
        cases = map(lambda p: (p - 1, p, p + 1), position)
        for neighbor in product(*cases):
            if neighbor != position:
                yield neighbor
                   
    def getLimits(self):
        limits = [ ]
        currentDimension = self
        while isinstance(currentDimension, Dimension):
            limits.append(currentDimension.getLimit())
            if len(currentDimension) == 0:
                break
            currentDimension = currentDimension[0]
        return tuple(limits)

    def isPositionActive(self, position):
        return self.isPositionValid(position) and self.getValue(position)

    def getValue(self, position):
        currentDimension = self
        for coordinate in position[:-1]:
            currentDimension = currentDimension[coordinate]
        return currentDimension[position[-1]]

    def setValue(self, position, value):
        currentDimension = self
        for coordinate in position[:-1]:
            currentDimension = currentDimension[coordinate]
        currentDimension[position[-1]] = value

    def getActiveCountForNeighbors(self, neighbors):
        return sum(map(lambda neighbor: self.isPositionActive(neighbor), neighbors))

    def copyGrowUniverse(self):
        newState = Universe()
        self[0].copyGrow(newState)
        for dimension in self:
            dimension.copyGrow(newState)
        self[0].copyGrow(newState)
        return newState
            
    def getNextStep(self):
        newState = self.copyGrowUniverse()
        limits = self.getLimits()
        dimensionCount = len(limits)

        position = []
        for limit in limits:
            position.append(limit[0] - 1)

        done = False
        while not done:
            neighbors = list(self.getNeighbors(tuple(position)))
            neighborsActiveCount = self.getActiveCountForNeighbors(neighbors)
            newValue = False
            if self.isPositionActive(position):
                newValue = neighborsActiveCount == 2 or neighborsActiveCount == 3
            else:
                newValue = neighborsActiveCount == 3
            newState.setValue(position, newValue)

            currentDimension = dimensionCount - 1
            while currentDimension >= 0:
                if position[currentDimension] < limits[currentDimension][1] + 1:
                    position[currentDimension] += 1
                    break
                elif currentDimension > 0:
                    position[currentDimension] = limits[currentDimension][0] - 1
                    currentDimension -= 1
                else:
                    done = True
                    break

        return newState

    def getActiveCount(self):
        activeCount = 0
        limits = self.getLimits()
        dimensionCount = len(limits)
        position = []
        for limit in limits:
            position.append(limit[0])

        done = False
        while not done:
            activeCount += self.getValue(tuple(position))
            currentDimension = 0
            while currentDimension < dimensionCount:
                if position[currentDimension] < limits[currentDimension][1]:
                    position[currentDimension] += 1
                    break
                elif currentDimension < dimensionCount - 1:
                    position[currentDimension] = limits[currentDimension][0]
                    currentDimension += 1
                else:
                    done = True
                    break
                
        return activeCount


def runCycles(universe):
    cycle = 0
    while cycle < 6:
        cycle += 1
        universe = universe.getNextStep()
    return universe.getActiveCount()

def part1(puzzleInput):
    return runCycles(puzzleInput)


def part2(puzzleInput):
    puzzleInput.addDimension()
    return runCycles(puzzleInput)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    universe = Universe()
    dimension = Dimension(universe)
    with open(filePath, "r") as file:
        for line in file.readlines():
            row = Dimension(dimension)
            for c in line.strip():
                row.append(True if c == "#" else False)

    return universe


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