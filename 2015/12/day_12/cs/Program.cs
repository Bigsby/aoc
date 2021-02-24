using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;
using System.Text.Json;


namespace AoC
{
    class Program
    {
        static Regex numberRegex = new Regex(@"(-?[\d]+)", RegexOptions.Compiled);
        static int Part1(string puzzleInput)
            => numberRegex.Matches(puzzleInput).Sum(match => int.Parse(match.Groups[0].Value));

        static int GetTotal(JsonElement obj)
        {
            if (obj.ValueKind == JsonValueKind.Object)
            {
                if (obj.EnumerateObject().Any(prop => prop.Value.ValueKind == JsonValueKind.String && prop.Value.GetString() == "red"))
                    return 0;
                return obj.EnumerateObject().Sum(prop => GetTotal(prop.Value));
            }
            if (obj.ValueKind == JsonValueKind.Number)
                return obj.GetInt32();
            if (obj.ValueKind == JsonValueKind.Array)
                return obj.EnumerateArray().Sum(item => GetTotal(item));
            return 0;
        }

        static int Part2(string puzzleInput)
            => GetTotal(JsonSerializer.Deserialize<JsonElement>(puzzleInput));
        
        static string GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim();
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