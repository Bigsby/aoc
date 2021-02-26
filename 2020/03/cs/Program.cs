using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using trees = IEnumerable<Complex>;
    class Program
    {
        static long CalculateTrees(trees trees, Complex step)
        {
            var yLimit = (int)trees.Select(position => position.Imaginary).Max() + 1;
            var xLimit = (int)trees.Select(position => position.Real).Max() + 1;
            Complex position = 0;
            var treeCount = 0;
            while (position.Imaginary < yLimit)
            {
                treeCount += trees.Contains(new Complex(position.Real % xLimit, position.Imaginary)) ? 1 : 0;
                position += step;
                
            }
            return treeCount;
        }
     
        static Complex[] STEPS = new[] {
            new Complex(1, 1),
            new Complex(3, 1),
            new Complex(5, 1),
            new Complex(7, 1),
            new Complex(1, 2)
        };
        static (long, long) Solve(trees trees)
            => (
                CalculateTrees(trees, new Complex(3, 1)),
                STEPS.Aggregate(1L, (soFar, step) => soFar * CalculateTrees(trees, step))
            );

        static trees GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            foreach(var (line, y) in File.ReadAllLines(filePath).Select((line, index) => (line, index)))
                foreach (var (c, x) in line.Select((c, index) => (c, index)))
                    if (c == '#')
                        yield return new Complex(x, y);
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