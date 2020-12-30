#! /usr/bin/python3

import sys, os, time
import re


class Replacement():
    def __init__(self, source, target):
        self.source = source
        self.target = target

    def __str__(self):
        return f"{self.source} -> {self.target}"
    def __repr__(self):
        return self.__str__()


def processReplacement(molecule, replacement):
    return processReplacementDirect(molecule, replacement.source, replacement.target)

    
def processReplacementDirect(molecule, source, target):
    return [ "".join([ molecule[0 : match.start()], target, molecule[match.end() : ] ]) for match in re.finditer(source, molecule) ]


def part1(puzzleInput):
    replacements, molecule = puzzleInput
    newMolecules = []
    for replacement in replacements:
        for newMolecule in processReplacement(molecule, replacement):
            newMolecules.append(newMolecule)

    return len(set(newMolecules))


def getValidReplacements(molecule, replacements):
    return [ replacement for replacement in replacements if replacement.target in molecule ]


class PointInSearch():
    def __init__(self, origin, replacements, replacement = None, parent = None):
        self.origin = origin
        self.parent = parent
        self.replacement = replacement
        self.validReplacements = getValidReplacements(origin, replacements)
        self.hasValidReplacements = len(self.validReplacements) != 0
        self.iteration = parent.iteration + 1 if parent else 0
        self.closed = False
        self.populated = False
        self.children = []
    
    def __str__(self):
        return f"{self.iteration} {self.hasValidReplacements} {self.origin} r:{len(self.replacements)} c:{len(self.children)}"
    def __repr__(self):
        return self.__str__()

    def generateChildren(self, replacements):
        for replacement in self.validReplacements:
            branches = processReplacementDirect(self.origin, replacement.target, replacement.source)
            for branch in branches:
                self.children.append(PointInSearch(branch, replacements, replacement, self))
        self.populated = True

    def getNextChild(self):
        childFound = next(filter(lambda c: not c.closed, self.children), None)
        return childFound

    def getNextPoint(self, childToRemove = None):
        if childToRemove:
            self.children.remove(childToRemove)
        if self.closed:
            return self.parent.getNextPoint(self)
        nextChild = self.getNextChild()
        if nextChild == None:
            if self.parent:
                return self.parent.getNextPoint(self)
            else:
                return None
        else:
            return nextChild


def part2(puzzleInput):
    replacements, targetMolecule = puzzleInput
    startingMolecule = "e"
    currentPoint = PointInSearch(targetMolecule, replacements)
    while currentPoint:        
        if not currentPoint.populated:
            currentPoint.generateChildren(replacements)
        if currentPoint.origin == startingMolecule:
            return currentPoint.iteration
        currentPoint = currentPoint.getNextPoint()


lineRegex = re.compile(r"^(\w+)\s=>\s(\w+)$")
def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        replacements = []
        molecule = ""
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                replacements.append(Replacement(*match.group(1, 2)))
            else:
                molecule += line
        return replacements, molecule.strip()


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