#! /usr/bin/python3


from common import getInput, createSolutionFromCombination, findValueForSolution, getPossibleCombinations


def main():
    entries = list(getInput())
    totalSpoons = 100
    ingredients = list(map(lambda entry: entry.name, entries))
    possibleCombinations = getPossibleCombinations(ingredients, totalSpoons)
    maxValue = 0
    for combination in possibleCombinations:
        solution = createSolutionFromCombination(combination, ingredients)
        solutionResult, _ = findValueForSolution(solution, entries)
        maxValue = max(maxValue, solutionResult)

    print("Highest score:", maxValue)


if __name__ == "__main__":
    main()
