#! /usr/bin/python3

import sys

from common import getInput, processReplacementDirect


class PointInSearch():
    def __init__(self, origin, replacements, replacement = None, parent = None):
        self.origin = origin
        self.parent = parent
        self.replacement = replacement
        self.replacements = getValidReplacements(origin, replacements)
        self.hasValidReplacements = len(self.replacements) != 0
        self.iteration = parent.iteration + 1 if parent else 0
        self.closed = False
        self.populated = False
        self.children = []

    
    def __str__(self):
        return f"{self.iteration} {self.hasValidReplacements} {self.origin} r:{len(self.replacements)} c:{len(self.children)}"
    def __repr__(self):
        return self.__str__()


    def generateChildren(self, replacements):
        for replacement in self.replacements:
            branches = list(processReplacementDirect(self.origin, replacement.target, replacement.source))
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
        

def getValidReplacements(molecule, replacements):
    return list(filter(lambda replacement: replacement.target in molecule, replacements))


def main():
    replacements, targetMolecule = getInput()
    startingMolecule = "e"
    
    currentPoint = PointInSearch(targetMolecule, replacements)
    iterations = sys.maxsize

    while currentPoint:        
        if not currentPoint.populated:
            currentPoint.generateChildren(replacements)
        if currentPoint.origin == startingMolecule:
            iterations = currentPoint.iteration
            break
        currentPoint = currentPoint.getNextPoint()

    print("Iterations:", iterations)


if __name__ == "__main__":
    main()
