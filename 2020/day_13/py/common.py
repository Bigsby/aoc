import sys, os, re


class Bus():
    index = 0

    def __init__(self, id):
        self.isX = id == "x"
        if self.isX:
            self.id = "x"
        else:
            self.id = int(id)
        self.index = Bus.index
        Bus.index = Bus.index + 1
          
    def __str__(self):
        return str(self.id)
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
        lines = file.readlines()
        return int(lines[0]), list(map(lambda id: Bus(id), lines[1].split(",")))
