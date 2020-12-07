#! /usr/bin/python3

from common import getInput, Operand


def main():
    startingTarget = "a"
    maxValue = pow(2, 16)
    circuit = getInput()
    aresult = circuit.solveFor(startingTarget)
    solutions = { "b": aresult }
    result = circuit.solveFor(startingTarget, solutions)
    if result < 0:
        result = maxValue + result
    print("Result for", startingTarget, ":", result)
    

if __name__ == "__main__":
    main()
