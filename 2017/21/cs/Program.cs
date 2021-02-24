using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Numerics;

namespace AoC
{
    using Grid = HashSet<Complex>;
    using Rules = Dictionary<int, List<Rule>>;
    record Rule(Grid match, Grid result);

    static class Program
    {
        const string START = ".#./..#/###";

        static void PrintGrid(Grid grid)
        {
            var maxX = (int)grid.Max(p => p.Real);
            var maxY = (int)grid.Max(p => p.Imaginary);
            for (var y = 0; y < maxY + 1; y++)
            {
                for (var x = 0; x < maxX + 1; x++)
                    Write(grid.Contains(new Complex(x, y)) ? '#' : '.');
                WriteLine();
            }
            WriteLine();
        }

        static (int, Grid grid) ParseGrid(string text)
        {
            var grid = new Grid();
            var split = text.Split('/');
            foreach (var (line, y) in split.Select((line, y) => (line, y)))
                foreach (var (c, x) in line.Select((c, x) => (c, x)))
                    if (c == '#')
                        grid.Add(new Complex(x, y));
            return (split[0].Length, grid);
        }

        static Grid MirrorHorizontal(Grid grid, int size)
            => grid.Select(position => new Complex(size - 1 - position.Real, position.Imaginary)).ToHashSet();
        
        static Grid RotateClockwise(Grid grid, int size)
            => grid.Select(position => new Complex(size - 1 - position.Imaginary, position.Real)).ToHashSet();

        static IEnumerable<Grid> GeneratePermutations(Grid grid, int size)
        {
            foreach (var _ in Enumerable.Range(0, 4))
            {
                yield return grid;
                yield return MirrorHorizontal(grid, size);
                grid = RotateClockwise(grid, size);
            }
        }

        static Grid EnhanceGrid(Grid grid, int size, IEnumerable<Rule> rules)
        {
            foreach (var permutation in GeneratePermutations(grid, size))
                foreach (var (match, result) in rules)
                    if (match.SetEquals(permutation))
                        return result;
            throw new Exception("Rule not found");
        }

        static IEnumerable<(int, int, Grid innerGrid)> SplitGrid(Grid grid, int count, int size)
        {
            for (var yIndex = 0; yIndex < count; yIndex++)
                for (var xIndex = 0; xIndex < count; xIndex++)
                {
                    var xOffset = xIndex * size;
                    var yOffset = yIndex * size;
                    var innerGrid = grid.Where(p => p.Real >= xOffset
                                                && p.Real < xOffset + size
                                                && p.Imaginary >= yOffset
                                                && p.Imaginary < yOffset + size)
                                        .Select(p => p - new Complex(xIndex * size, yIndex * size))
                                        .ToHashSet();
                    yield return (xIndex, yIndex, innerGrid);
                }
        }

        static (int, Grid) Iterate(Grid grid, int size, Rules rules)
        {
            var enhancedGrid = new Grid();
            var divider = 0;
            var ruleSize = 0;
            if (size % 2 == 0)
                ruleSize = 2;
            else if (size % 3 == 0)
                ruleSize = 3;
            var ruleSet = rules[ruleSize];
            divider = size / ruleSize;
            foreach (var (xIndex, yIndex, innerGrid) in SplitGrid(grid, divider, ruleSize))
                foreach (var position in EnhanceGrid(innerGrid, ruleSize, ruleSet))
                    enhancedGrid.Add(position + xIndex * (ruleSize + 1) + yIndex * Complex.ImaginaryOne * (ruleSize + 1));
            return (size + divider, enhancedGrid);
        }

        static (int, Grid grid) RunIterations(Grid grid, int size, Rules rules, int iterations)
        {
            foreach (var _ in Enumerable.Range(0, iterations))
                (size, grid) = Iterate(grid, size, rules);
            return (size, grid);
        }

        static int Part1(Rules rules)
        {
            var (size, grid) = ParseGrid(START);
            return RunIterations(grid, size, rules, 5).grid.Count;
        }

        static IEnumerable<Grid> RunNext3Iterations(Grid grid, Rules rules)
            => SplitGrid(RunIterations(grid, 3, rules, 3).grid, 3, 3).Select(split => split.innerGrid);

        static int GetGridId(Grid grid)
            => grid.Sum(p => 1 << (int)p.Real << 3 * (int)p.Imaginary);

        static int Part2(Rules rules)
        {
            var grid = ParseGrid(START).grid;
            var total = 0;
            var calculated = new Dictionary<int, Grid[]>();
            var queue = new Stack<(Grid, int)>();
            queue.Push((grid, 0));
            var iterations = 0;
            while (queue.Any())
            {
                (grid, iterations) = queue.Pop();
                if (iterations == 18)
                    total += grid.Count;
                else
                {
                    var gridId = GetGridId(grid);
                    if (!calculated.ContainsKey(gridId))
                        calculated[gridId] = RunNext3Iterations(grid, rules).ToArray();
                    foreach (var innerGrid in calculated[gridId])
                        queue.Push((innerGrid, iterations + 3));
                }
            }
            return total;
        }

        static Regex lineRegex = new Regex(@"^(?<rule>[./#]+) => (?<result>[./#]+)$", RegexOptions.Compiled);
        static Rules GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var rules = new Dictionary<int, List<Rule>>();
            rules[2] = new List<Rule>();
            rules[3] = new List<Rule>();
            foreach (var line in File.ReadLines(filePath))
            {
                var match = lineRegex.Match(line);
                var (ruleSize, ruleGrid) = ParseGrid(match.Groups["rule"].Value);
                var (_, resultGrid) = ParseGrid(match.Groups["result"].Value);
                rules[ruleSize].Add(new Rule(ruleGrid, resultGrid));
            }
            return rules;
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
