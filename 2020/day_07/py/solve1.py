#! /usr/bin/python3

from common import getInput


requiredColor = "shiny gold"


def getRulesContaining(color, rules):
    for rule in rules:
        if any(map(lambda innerRule: innerRule.color == color and innerRule.quantity > 0, rule.innerRules)):
            yield rule
            yield from getRulesContaining(rule.color, rules)


def removeDuplicates(rules):
    ruleColors = map(lambda rule: rule.color, rules)
    return list(set(ruleColors))


def main():
    rules = list(getInput())
    hierarchyRules  = list(getRulesContaining(requiredColor, rules))
    noDuplicates = removeDuplicates(hierarchyRules)
    containingRulesCount = len(noDuplicates)
    print("Containing count:", containingRulesCount)


if __name__ == "__main__":
    main()
