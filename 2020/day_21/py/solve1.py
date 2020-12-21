#! /usr/bin/python3

from functools import reduce

from common import getInput


def main():
    foods = list(getInput())
    allergens = set()
    for food in foods:
        for allergen in food.allergens:
            allergens.add(allergen)

    allergenGraph = {
        allergen: reduce(lambda soFar, foodAllergens: soFar & foodAllergens, \
            (set(food.ingredients) for food in foods if allergen in food.allergens)) \
            for allergen in allergens
    }

    foundIngredients = reduce(lambda soFar, ingredientsForAllergen: soFar | ingredientsForAllergen, (allergenGraph[allergen] for allergen in allergenGraph))

    count = 0
    for food in foods:
        for ingredient in food.ingredients:
            count += ingredient not in foundIngredients
    print("Ingredients without allergens count:", count)

        

if __name__ == "__main__":
    main()
