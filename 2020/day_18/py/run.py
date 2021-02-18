#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


def getNextToken(expression: str) -> Tuple[str,str]:
    currentToken = ""
    for index, c in enumerate(expression):
        if c == " ":
            return currentToken, expression[index + 1:].strip()
        if currentToken.isdigit() and not c.isdigit():
            return currentToken, expression[index:].strip()
        currentToken += c
    return currentToken, ""
        

def performOperation(first: int, operation: str, second: int) -> int:
    if operation == "*":
        return first * second
    if operation == "+":
        return first + second
    raise Exception(f"Unknow operation {operation}")
        

parenRegex = re.compile(r"\((?P<expression>[^()]+)\)")
plusRegex = re.compile(r"(?P<first>\d+)\s\+\s(?P<second>\d+)")
def evaluateExpression(expression: str, addFirst: bool) -> int:
    parenMatch = parenRegex.search(expression)
    while parenMatch:
        expression = "".join([expression[:parenMatch.start()], str(evaluateExpression(parenMatch.group("expression"), addFirst)), expression[parenMatch.end():]])
        parenMatch = parenRegex.search(expression)

    if addFirst:
        plusMatch = plusRegex.search(expression)
        while plusMatch:
            expression = "".join([expression[:plusMatch.start()], str(int(plusMatch.group("first")) + int(plusMatch.group("second"))), expression[plusMatch.end():]])
            plusMatch = plusRegex.search(expression)

    token, expression = getNextToken(expression)
    currentValue = int(token)
    operationToPeform = ""
    while expression:
        token, expression = getNextToken(expression)
        if token.isdigit():
            currentValue = performOperation(currentValue, operationToPeform, int(token))
        else:
            operationToPeform = token
    return currentValue


def evaluateExpressions(addFirst: bool, expressions: List[str]) -> int:
    return sum([ evaluateExpression(line, addFirst) for line in expressions ])
    

def part1(expressions: List[str]) -> int:
    return evaluateExpressions(False, expressions)


def part2(expression: List[str]) -> int:
    return evaluateExpressions(True, expression)


def getInput(filePath: str) -> List[str]:
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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()