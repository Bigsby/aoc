using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Entry(string name, int capacity, int durability, int flavor, int texture, int calories);

    class Program
    {
        static int GetValueForProperty(Dictionary<string, int> solution, IEnumerable<Entry> entries, string property)
            => entries.Aggregate(0, (soFar, entry) => 
                soFar + solution[entry.name] * (int)typeof(Entry).GetProperty(property).GetValue(entry));

        static string[] VALUE_PROPERTIES = new [] { "capacity", "durability", "flavor", "texture" };
        static (int score, int calories) FindValueForSolution(Dictionary<string, int> solution, IEnumerable<Entry> entries)
        {
            var values = new Dictionary<string, int>();
            foreach (var property in VALUE_PROPERTIES)
                values[property] = GetValueForProperty(solution, entries, property);
            var totalScore = values.Aggregate(1, (soFar, pair) => soFar * (pair.Value > 0 ? pair.Value : 0));
            var calories = GetValueForProperty(solution, entries, "calories");
            return (totalScore, calories);
        }

        static List<List<T>> GenerateCombinations<T>(IEnumerable<T> combinationList, int k)
        {
            var combinations = new List<List<T>>();
            if (k == 0)
            {
                var emptyCombination = new List<T>();
                combinations.Add(emptyCombination);
                return combinations;
            }
            if (combinationList.Count() == 0)
                return combinations;
            var head = combinationList.First();
            var copiedCombinationList = new List<T>(combinationList);
            var subcombinations = GenerateCombinations(copiedCombinationList, k - 1);
            foreach (var subcombination in subcombinations)
            {
                subcombination.Insert(0, head);
                combinations.Add(subcombination);
            }
            combinationList = combinationList.Skip(1);
            combinations.AddRange(GenerateCombinations(combinationList, k));
            return combinations;
        }

        static Dictionary<string, int> CreateSolutionFromCombination(IEnumerable<string> combination, IEnumerable<string> ingredients)
            => ingredients.ToDictionary(ingredient => ingredient, ingredient => combination.Count(i => i == ingredient));

        static (IEnumerable<string> ingredients, IEnumerable<IEnumerable<string>> combination) GetIngredientCombinations(IEnumerable<Entry> entries, int totalSpoons)
        {
            var ingredients = entries.Select(entry => entry.name);
            return (ingredients, GenerateCombinations(ingredients, totalSpoons));
        }
    
        static (int, int) Solve(IEnumerable<Entry> entries)
        {
            var (ingredients, possibleCombinations) = GetIngredientCombinations(entries, 100);
            int part1 = 0, part2 = 0;
            foreach (var combination in possibleCombinations)
            {
                var solution = CreateSolutionFromCombination(combination, ingredients);
                var (result, calories) = FindValueForSolution(solution, entries);
                part1 = Math.Max(part1, result);
                if (calories == 500)
                    part2 = Math.Max(part2, result);
            }
            return (part1, part2);
        }

        static Regex lineRegex = new Regex(@"^(\w+):\scapacity\s(-?\d+),\sdurability\s(-?\d+),\sflavor\s(-?\d+),\stexture\s(-?\d+),\scalories\s(-?\d+)$", RegexOptions.Compiled);
        static IEnumerable<Entry> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Entry(
                        match.Groups[1].Value,
                        int.Parse(match.Groups[2].Value),
                        int.Parse(match.Groups[3].Value),
                        int.Parse(match.Groups[4].Value),
                        int.Parse(match.Groups[5].Value),
                        int.Parse(match.Groups[6].Value)
                    );
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