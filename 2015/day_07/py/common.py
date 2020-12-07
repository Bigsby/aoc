import sys, os, re


sourceTargetRegex = re.compile("^(.*)\s->\s(\w+)$")
inputRegex = re.compile("^[^\s]+$")
unaryRegex = re.compile("NOT\s(\w+)$")
binaryRegex = re.compile("^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)")
binaryOperations = [ "AND", "OR", "LSHIFT", "RSHIFT" ]


class Operand():
    def __init__(self, value):
        try:
            self.value = int(value)
            self.type = "scalar"
        except:
            self.value = value
            self.type = "wire"
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return self.__str__()


class Connection():
    def __init__(self, operation, operand1, operand2, target):
        self.isInput = operation == None
        self.isUnary = operation == "NOT"
        self.isBinary = operation in binaryOperations
        self.operation = operation
        self.operand1 = Operand(operand1)
        self.operand2 = Operand(operand2)
        self.target = target
    def __str__(self):
        if self.isInput:
            return f"{self.operand1} -> {self.target}"
        if self.isUnary:
            return f"NOT {self.operand1} -> {self.target}"
        return f"{self.operand1} {self.operation} {self.operand2} -> {self.target}"
    def __repr__(self):
        return self.__str__()


def processLine(line):
    sourceTargetMatch = sourceTargetRegex.match(line)
    if sourceTargetMatch:
        source, target = sourceTargetMatch.group(1, 2)
        if inputRegex.match(source):
            return Connection(None, source, None, target)
        unaryMatch = unaryRegex.match(source)
        if unaryMatch:
            return Connection("NOT", unaryMatch.group(1), None, target)
        binaryMatch = binaryRegex.match(source)
        if binaryMatch:
            return Connection(binaryMatch.group(2), binaryMatch.group(1), binaryMatch.group(3), target)
        raise Exception("Unrecognized operation:", source)
    else:
        raise Exception("Unrecognized operation line:", line)


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
            yield processLine(line)
            
