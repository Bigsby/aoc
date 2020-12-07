#! /usr/bin/python3


from functools import reduce


from common import getInput


def getRuleForColor(color, rules):
    return next(filter(lambda rule: rule.color == color, rules), None)
    

def getQuantityFromColor(color, rules):
    colorRule = getRuleForColor(color, rules)
    bagCount = reduce(lambda currentCount, innerRule: currentCount + innerRule.quantity, colorRule.innerRules, 0)
    for innerRule in colorRule.innerRules:
        bagCount = bagCount + innerRule.quantity * getQuantityFromColor(innerRule.color, rules)
    return bagCount


def main():
    rules = list(getInput())
    containedBagsCount = getQuantityFromColor("shiny gold", rules)
    print("Bags in shiny gold:", containedBagsCount)


if __name__ == "__main__":
    main()
