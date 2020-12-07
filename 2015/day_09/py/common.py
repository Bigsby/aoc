import sys, os, re
from itertools import permutations


lineRegex = re.compile("^(.*)\sto\s(.*)\s=\s(\d+)$")

def getPathDistance(permutation, paths):
    distance = 0
    for index in range(0, len(permutation) - 1):
        path = next(filter(lambda p: p.nodeA == permutation[index] and p.nodeB == permutation[index + 1] or p.nodeA == permutation[index + 1] and p.nodeB == permutation[index], paths))
        distance = distance + path.distance
    return distance


def getSingleNodes(edges):
    nodes = []
    for path in edges:
        nodes.append(path.nodeA)
        nodes.append(path.nodeB)
    return list(set(nodes))
 

def getPossiblePaths(nodes):
    return permutations(nodes, len(nodes))


class Edge():
    def __init__(self, nodeA, nodeB, distance):
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.distance = int(distance)

    def __str__(self):
        return f"{self.nodeA} - {self.nodeB} = {self.distance}"

    def __repr__(self):
        return self.__str__()


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            match = lineRegex.match(line)
            yield Edge(match.group(1), match.group(2), match.group(3))
