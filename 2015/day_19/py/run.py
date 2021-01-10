#! /usr/bin/python3

import sys, os, time
from typing import List, Optional, Tuple
import re


class Replacement():
    def __init__(self, source: str, target: str):
        self.source = source
        self.target = target


def processReplacement(molecule: str, replacement: Replacement) -> List[str]:
    return processReplacementDirect(molecule, replacement.source, replacement.target)

    
def processReplacementDirect(molecule: str, source: str, target: str) -> List[str]:
    return [ "".join([ molecule[0 : match.start()], target, molecule[match.end() : ] ]) for match in re.finditer(source, molecule) ]


def part1(puzzleInput: Tuple[List[Replacement],str]) -> int:
    replacements, molecule = puzzleInput
    newMolecules = []
    for replacement in replacements:
        for newMolecule in processReplacement(molecule, replacement):
            newMolecules.append(newMolecule)

    return len(set(newMolecules))


def getValidReplacements(molecule: str, replacements: List[Replacement]) -> List[Replacement]:
    return [ replacement for replacement in replacements if replacement.target in molecule ]


class PointInSearch():
    def __init__(self, origin: str, replacements: List[Replacement], replacement: Optional[Replacement] = None, parent: Optional['PointInSearch'] = None):
        self.origin = origin
        self.parent = parent
        self.replacement = replacement
        self.validReplacements = getValidReplacements(origin, replacements)
        self.hasValidReplacements = len(self.validReplacements) != 0
        if parent:
            self.iteration = parent.iteration + 1
        else:
            self.iteration = 0
        self.closed = False
        self.populated = False
        self.children = []

    def generateChildren(self, replacements: List[Replacement]):
        for replacement in self.validReplacements:
            branches = processReplacementDirect(self.origin, replacement.target, replacement.source)
            for branch in branches:
                self.children.append(PointInSearch(branch, replacements, replacement, self))
        self.populated = True

    def getNextChild(self) -> Optional['PointInSearch']:
        return next(filter(lambda c: not c.closed, self.children), None)

    def getNextPoint(self, childToRemove: Optional['PointInSearch'] = None) -> Optional['PointInSearch']:
        if childToRemove:
            self.children.remove(childToRemove)
        if self.closed and self.parent:
            return self.parent.getNextPoint(self)
        nextChild = self.getNextChild()
        if nextChild:
            return nextChild
        if self.parent:
            return self.parent.getNextPoint(self)
        return None            


def part2(puzzleInput: Tuple[List[Replacement],str]):
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
def getInput(filePath: str) -> Tuple[List[Replacement],str]:
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