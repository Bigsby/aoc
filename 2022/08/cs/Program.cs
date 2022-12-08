using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = Dictionary<Complex, int>;

    static class Program
    {
        static Complex[] DIRECTIONS = new [] {
            new Complex(-1, 0),
            new Complex(0, -1),
            new Complex(1, 0),
            new Complex(0, 1)
        };

        static bool IsVisible(Input trees, int xMax, int yMax, Complex tree, Complex direction)
        {
            var treeHeight = trees[tree];
            var test = tree + direction;
            while (0 <= test.Real && test.Real <= xMax && 0 <= test.Imaginary && test.Imaginary <= yMax)
            {
                if (trees[test] >= treeHeight)
                    return false;
                test += direction;
            }
            return true;
        }

        static int Part1(Input trees, int xMax, int yMax)
        { 
            var visibleTrees = 2 * xMax + 2 * yMax;
            for (var x = 1; x < xMax; x++)
                for (var y = 1; y < yMax; y++)
                    foreach (var direction in DIRECTIONS)
                        if (IsVisible(trees, xMax, yMax, new Complex(x, y), direction))
                        {
                            visibleTrees++;
                            break;
                        }
            return visibleTrees;
        }

        static int GetScenicScore(Input trees, int xMax, int yMax, Complex tree)
        {
            var scenicScore = 1;
            var treeHeight = trees[tree];
            foreach (var direction in DIRECTIONS)
            {
                var test = tree + direction;
                var directionScore = 0;
                while (0 <= test.Real && test.Real <= xMax && 0 <= test.Imaginary && test.Imaginary <= yMax)
                {
                    directionScore++;
                    if (trees[test] >= treeHeight)
                        break;
                    test += direction;
                }
                scenicScore *= directionScore;
            }
            return scenicScore;
        }

        static int Part2(Input trees, int xMax, int yMax)
        {
            var maxScenicScore = 0;
            for (var x = 1; x < xMax; x++)
                for (var y = 1; y < yMax; y++)
                    maxScenicScore = Math.Max(maxScenicScore, GetScenicScore(trees, xMax, yMax, new Complex(x, y)));
            return maxScenicScore;
        }

        static (int, int) Solve(Input trees)
        {
            var xMax = (int)trees.Max(pair => pair.Key.Real);
            var yMax = (int)trees.Max(pair => pair.Key.Imaginary);
            return (Part1(trees, xMax, yMax), Part2(trees, xMax, yMax));
        }

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var trees = new Dictionary<Complex, int>();
            var tree = new Complex(0, 0);
            foreach(var line in File.ReadAllLines(filePath))
            {
                foreach(var c in line)
                {
                    trees[tree] = c - '0';
                    tree += 1;
                }
                tree = new Complex(0, tree.Imaginary + 1);
            }
            return trees;
        }

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
