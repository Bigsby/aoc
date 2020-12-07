#! /usr/bin/python3

from common import getInput


def main():
    startingTarget = "a"
    maxValue = pow(2, 16)
    circuit = getInput()
    result = circuit.solveFor("a")
    if result < 0:
        result = maxValue + result
    print("Result for", startingTarget, ":", result)
    

if __name__ == "__main__":
    main()
