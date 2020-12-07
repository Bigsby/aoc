import sys, os, re


sourceTargetRegex = re.compile("^(.*)\s->\s(\w+)$")
inputRegex = re.compile("^[^\s]+$")
unaryRegex = re.compile("NOT\s(\w+)$")
binaryRegex = re.compile("^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)")
binaryOperations = [ "AND", "OR", "LSHIFT", "RSHIFT" ]


class Circuit():
    def __init__(self, connections):
        self.connections = list(connections)
        self.solutions = {}

    def getConnectionFromTarget(self, target):
        return next(filter(lambda conn: conn.target == target, self.connections), None)

    def getConnectionFromOperand(self, operand):
        if operand and operand.type == "wire":
            return self.getConnectionFromTarget(operand.value)
        return None

    def getValueFromOperand(self, operand):
        if operand.type == "scalar":
            return operand.value
        return self.getValueFromConnection(self.getConnectionFromTarget(operand.value))

    binaryOperations = {
        "AND": lambda x, y: x & y,
        "OR": lambda x, y: x | y,
        "LSHIFT": lambda x, y: x << y,
        "RSHIFT": lambda x, y: x >> y
    }
    def getValueFromBinaryConneciton(self, connection):
        operation = Circuit.binaryOperations[connection.operation]
        return operation(self.getValueFromOperand(connection.operand1), self.getValueFromOperand(connection.operand2))

    def getNewValueForConnection(self, connection):
        if connection.type == "input":
            return self.getValueFromOperand(connection.operand1)
        if connection.type == "unary":
            return ~self.getValueFromOperand(connection.operand1)
        if connection.type == "binary":
            return self.getValueFromBinaryConneciton(connection)
        raise Exception("Unknown operation:", connection)

    def getValueFromConnection(self, connection):
        if connection.target in self.solutions:
            return self.solutions[connection.target]
        result = self.getNewValueForConnection(connection)
        self.solutions[connection.target] = result
        return result

    def solveFor(self, target, initialState = {}):
        self.solutions = initialState
        return self.getValueFromConnection(self.getConnectionFromTarget(target))


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
    def __init__(self, operation, type, operand1, operand2, target):
        self.operation = operation
        self.type = type
        self.operand1 = Operand(operand1)
        self.operand2 = Operand(operand2)
        self.target = target
    def __str__(self):
        if self.type == "input":
            return f"{self.operand1} -> {self.target}"
        if self.type == "unary":
            return f"NOT {self.operand1} -> {self.target}"
        return f"{self.operand1} {self.operation} {self.operand2} -> {self.target} ({self.type})"
    def __repr__(self):
        return self.__str__()


def processLine(line):
    sourceTargetMatch = sourceTargetRegex.match(line)
    if sourceTargetMatch:
        source, target = sourceTargetMatch.group(1, 2)
        if inputRegex.match(source):
            return Connection(None, "input", source, None, target)
        unaryMatch = unaryRegex.match(source)
        if unaryMatch:
            return Connection("NOT", "unary", unaryMatch.group(1), None, target)
        binaryMatch = binaryRegex.match(source)
        if binaryMatch:
            return Connection(binaryMatch.group(2), "binary", binaryMatch.group(1), binaryMatch.group(3), target)
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
        return Circuit(map(lambda line: processLine(line), file.readlines()))
