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

        static int Part1(IEnumerable<Food> foods, Dictionary<string, HashSet<string>> allergenGraph)
        {
            var foundIngredients = allergenGraph.Values.Aggregate(new HashSet<string>(), 
                (soFar, ingredientsForAllergen) => soFar.Union(ingredientsForAllergen).ToHashSet());
            return foods.Sum(food => food.ingredients.Count(ingredient => !foundIngredients.Contains(ingredient)));
        }

        static string Part2(Dictionary<string, HashSet<string>> allergenGraph)
        {
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

        static (int, string) Solve(IEnumerable<Food> foods)
        {
            var allergenGraph = BuildAllergenGraph(foods);
            return (
                Part1(foods, allergenGraph),
                Part2(allergenGraph)
            );
        }

        static Regex lineRegex = new Regex(@"^(?<ingredients>[^\(]+)\s\(contains\s(?<allergens>[^\)]+)\)$", RegexOptions.Compiled);
        static IEnumerable<Food> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Food(match.Groups["ingredients"].Value.Split(" "), match.Groups["allergens"].Value.Split(", "));
                throw new Exception($"Bad format '{line}'");
            });

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var watch = Stopwatch.StartNew();
            var (part1Result, part2Result) = Solve(GetInput(args[0]));
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"Time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}
