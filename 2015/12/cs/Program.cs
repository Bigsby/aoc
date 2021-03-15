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
                if (obj.EnumerateObject().Any(prop => prop.Value.ValueKind == JsonValueKind.String
                    && prop.Value.GetString() == "red"))
                    return 0;
                return obj.EnumerateObject().Sum(prop => GetTotal(prop.Value));
            }
            if (obj.ValueKind == JsonValueKind.Number)
                return obj.GetInt32();
            if (obj.ValueKind == JsonValueKind.Array)
                return obj.EnumerateArray().Sum(item => GetTotal(item));
            return 0;
        }

        static (int, int) Solve(string puzzleInput)
            => (
                numberRegex.Matches(puzzleInput).Sum(match => int.Parse(match.Groups[0].Value)),
                GetTotal(JsonSerializer.Deserialize<JsonElement>(puzzleInput))
            );

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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