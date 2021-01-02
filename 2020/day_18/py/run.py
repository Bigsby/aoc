#! /usr/bin/python3

import sys, os, time
import re


def getNextToken(line):
    currentToken = ""
    for index, c in enumerate(line):
        if c == " ":
            return currentToken, line[index + 1:].strip()
        if currentToken.isdigit() and not c.isdigit():
            return currentToken, line[index:].strip()
        currentToken = "".join([currentToken, c])
    return currentToken, ""
        

def performOperation(first, operation, second):
    if operation == "*":
        return first * second
    if operation == "+":
        return first + second
    raise Exception(f"Unknow operation {operation}")
        

parenRegex = re.compile(r"\((?P<expression>[^()]+)\)")
plusRegex = re.compile(r"(?P<first>\d+)\s\+\s(?P<second>\d+)")
def evaluateExpression(text, addFirst):
    match = parenRegex.search(text)
    while match:
        text = "".join([text[:match.start()], str(evaluateExpression(match.group("expression"), addFirst)), text[match.end():]])
        match = parenRegex.search(text)

    if addFirst:
        match = plusRegex.search(text)
        while match:
            text = "".join([text[:match.start()], str(int(match.group("first")) + int(match.group("second"))), text[match.end():]])
            match = plusRegex.search(text)

    token, text = getNextToken(text)
    currentValue = int(token)
    operationToPeform = None
    while text:
        token, text = getNextToken(text)
        if token.isdigit():
            currentValue = performOperation(currentValue, operationToPeform, int(token))
        else:
            operationToPeform = token
    return currentValue


def evaluateExpressions(addFirst, puzzleInput):
    return sum([ evaluateExpression(line, addFirst) for line in puzzleInput ])
    

def part1(puzzleInput):
    return evaluateExpressions(False, puzzleInput)


def part2(puzzleInput):
    return evaluateExpressions(True, puzzleInput)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.readlines()


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