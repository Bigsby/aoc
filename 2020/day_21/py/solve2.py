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
        allergenGraph[allergen] = list(reduce(lambda soFar, foodAllergens: soFar & foodAllergens, (set(food.ingredients) for food in foods if allergen in food.allergens)))


    while any([len(ingredients) != 1 for _, ingredients in allergenGraph.items()]):
        singleIngredientAllergens = [ (allergen, allergenGraph[allergen][0]) for allergen in allergenGraph if len(allergenGraph[allergen]) == 1 ]
        for singleAllergen, ingredients in singleIngredientAllergens:
            ingredient = ingredients
            for allergen in allergenGraph:
                if allergen != singleAllergen and ingredient in allergenGraph[allergen]:
                    allergenGraph[allergen].remove(ingredient)
    
    sortedKeys = sorted(allergenGraph)               
    result = ",".join(map(lambda k: allergenGraph[k][0], sortedKeys))
    print("Canonical dangerous ingredient list:")
    print(result)
            
if __name__ == "__main__":
    main()
