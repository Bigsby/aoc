#! /usr/bin/python3

from common import getInput


def getConnectionFromTarget(target, connections):
    return next(filter(lambda conn: conn.target == target, connections), None)


def getConnectionFromOperand(operand, connections, solutions):
    if operand and operand.type == "wire":
        return getConnectionFromTarget(operand.value, connections, solutions)
    return None
   

def getValueFromOperand(operand, connections, solutions):
    if operand.type == "scalar":
        return operand.value
    return getValueFromConnection(getConnectionFromTarget(operand.value, connections), connections, solutions)


binaryOperations = {
    "AND": lambda x, y: x & y,
    "OR": lambda x, y: x | y,
    "LSHIFT": lambda x, y: x << y,
    "RSHIFT": lambda x, y: x >> y
}
def getValueFromBinaryConneciton(connection, connections, solutions):
    operation = binaryOperations[connection.operation]
    return operation(getValueFromOperand(connection.operand1, connections, solutions), getValueFromOperand(connection.operand2, connections, solutions))
    

def getValueFromConnection(connection, connections, solutions = {}):
    if connection.target in solutions:
        return solutions[connection.target]
    result = 0
    if connection.isInput:
        result = getValueFromOperand(connection.operand1, connections, solutions)
    if connection.isUnary:
        result = ~getValueFromOperand(connection.operand1, connections, solutions)
    if connection.isBinary:
        result = getValueFromBinaryConneciton(connection, connections, solutions)
    solutions[connection.target] = result
    return result


def main():
    startingTarget = "a"
    maxValue = pow(2, 16)
    connections = list(getInput())
    startingConnection = getConnectionFromTarget(startingTarget, connections)
    result = getValueFromConnection(startingConnection, connections)
    if result < 0:
        result = maxValue + result
    print("Result for", startingTarget, ":", result)
    

if __name__ == "__main__":
    main()
