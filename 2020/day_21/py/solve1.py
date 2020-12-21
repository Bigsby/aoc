#! /usr/bin/python3

from functools import reduce

from common import getInput


def main():
    foods = list(getInput())
    ingredients = set()
    allergens = set()
    for food in foods:
        for ingredient in food.ingredients:
            ingredients.add(ingredient)
        for allergen in food.allergens:
            allergens.add(allergen)

    allergenGraph = {}
    for allergen in allergens:
        allergenGraph[allergen] = reduce(lambda soFar, foodAllergens: soFar & foodAllergens, (set(food.ingredients) for food in foods if allergen in food.allergens))

    foundIngredients = reduce(lambda soFar, ingredientsForAllergen: soFar | ingredientsForAllergen, (ingredientsInAllergen for allergen, ingredientsInAllergen in allergenGraph.items()))

    count = 0
    for food in foods:
        for ingredient in food.ingredients:
            count += ingredient not in foundIngredients
    print("Ingredients without allergens count:", count)

        

if __name__ == "__main__":
    main()
