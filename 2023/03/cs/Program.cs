using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<string>;

    static class Program
    {
        static bool IsSymbol(char c)
            => c != '.' && !char.IsDigit(c);

        static (Dictionary<(int, int), List<int>>, List<int>) ParseEngine(Input puzzleInput)
        {
            var gears = new Dictionary<(int, int), List<int>>();
            var parts = new List<int>();
            foreach (var lineIndex in Enumerable.Range(0, puzzleInput.Count()))
            {
                var line = puzzleInput.ElementAt(lineIndex);
                var lineLength = line.Length;
                var startIndex = 0;
                while (startIndex < lineLength && !char.IsDigit(line[startIndex]))
                    startIndex++;
                while (startIndex < lineLength)
                {
                    var length = 1;
                    while (startIndex + length <= lineLength && line[startIndex..(startIndex + length)].All(char.IsDigit))
                        length++;
                    var segment = line[startIndex..(startIndex + length - 1)];
                    if (segment.All(char.IsDigit))
                    {
                        var searchStart = Math.Max(0, startIndex - 1);
                        var searchEnd = Math.Min(lineLength, startIndex + length);
                        var isPart = false;
                        var symbol = '\0';
                        var coord = (0, 0);
                        if (lineIndex > 0)
                            foreach (var (c, i) in puzzleInput.ElementAt(lineIndex - 1)[searchStart..searchEnd].Select((c, i) => (c, i)))
                                if (IsSymbol(c))
                                {
                                    isPart = true;
                                    symbol = c;
                                    coord = (searchStart + i, lineIndex - 1);
                                    break;
                                }
                        if (startIndex > 0 && IsSymbol(line[searchStart]))
                        {
                            isPart = true;
                            symbol = line[searchStart];
                            coord = (searchStart, lineIndex);
                        }
                        if (startIndex + length < lineLength && IsSymbol(line[searchEnd - 1]))
                        {
                            isPart = true;
                            symbol = line[searchEnd - 1];
                            coord = (searchEnd - 1, lineIndex);
                        }
                        if (!isPart && lineIndex < puzzleInput.Count() - 1)
                            foreach (var (c, i) in puzzleInput.ElementAt(lineIndex + 1)[searchStart..searchEnd].Select((c, i) => (c, i)))
                                if (IsSymbol(c))
                                {
                                    isPart = true;
                                    symbol = c;
                                    coord = (searchStart + i, lineIndex + 1);
                                    break;
                                }
                        if (isPart && segment.Length > 0)
                        {
                            var partNumber = int.Parse(segment);
                            parts.Add(partNumber);
                            if (symbol == '*')
                            {
                                if (!gears.ContainsKey(coord))
                                    gears[coord] = new List<int>();
                                gears[coord].Add(partNumber);
                            }
                        }
                    }
                    startIndex += length;
                }
            }
            return (gears, parts);
        }

        static int Part2((Dictionary<(int, int), List<int>>, List<int>) engineData)
            => engineData.Item1.Values.Where(parts => parts.Count() == 2).Sum(parts => parts.ElementAt(0) * parts.ElementAt(1));

        static (int, int) Solve(Input puzzleInput)
        {
            var engineData = ParseEngine(puzzleInput);
            return (engineData.Item2.Sum(), Part2(engineData));
        }

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Trim());

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
