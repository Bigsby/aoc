using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Food(IEnumerable<string> ingredients, IEnumerable<string> allergens);

    static class Program
    {
        static Dictionary<string, HashSet<string>> BuildAllergenGraph(IEnumerable<Food> foods)
            => foods.SelectMany(food => food.allergens).ToHashSet().ToDictionary(
                allergen => allergen, 
                allergen => foods.Where(food => food.allergens.Contains(allergen))
                    .Aggregate(new HashSet<string>(), 
                        (soFar , food) => soFar.Any() ? soFar.Intersect(food.ingredients).ToHashSet() : food.ingredients.ToHashSet()));

        static int Part1(IEnumerable<Food> foods)
        {
            var allergenGraph = BuildAllergenGraph(foods);
            var foundIngredients = allergenGraph.Values.Aggregate(new HashSet<string>(), 
                (soFar, ingredientsForAllergen) => soFar.Union(ingredientsForAllergen).ToHashSet());
            return foods.Sum(food => food.ingredients.Count(ingredient => !foundIngredients.Contains(ingredient)));
        }

        static string Part2(IEnumerable<Food> foods)
        {
            var allergenGraph = BuildAllergenGraph(foods);
            while (allergenGraph.Values.Any(ingredients => ingredients.Count != 1))
            {
                var singleIngredientAllergens = allergenGraph.Where(pair => pair.Value.Count == 1).Select(pair => (pair.Key, pair.Value.First()));
                foreach (var (singleAllergen, ingredient) in singleIngredientAllergens)
                    foreach (var pair in allergenGraph)
                        if (pair.Key != singleAllergen)
                            pair.Value.Remove(ingredient);
            }
            return string.Join(",", allergenGraph.OrderBy(pair => pair.Key).Select(pair => pair.Value.First()));
        }

        static Regex lineRegex = new Regex(@"^(?<ingredients>[^\(]+)\s\(contains\s(?<allergens>[^\)]+)\)$", RegexOptions.Compiled);
        static IEnumerable<Food> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Food(match.Groups["ingredients"].Value.Split(" "), match.Groups["allergens"].Value.Split(", "));
                throw new Exception($"Bad format '{line}'");
            });
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var puzzleInput = GetInput(args[0]);
            var watch = Stopwatch.StartNew();
            var part1Result = Part1(puzzleInput);
            watch.Stop();
            var middle = watch.ElapsedTicks;
            watch = Stopwatch.StartNew();
            var part2Result = Part2(puzzleInput);
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"P1 time: {(double)middle / 100 / TimeSpan.TicksPerSecond:f7}");
            WriteLine($"P2 time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}
