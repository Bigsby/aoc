using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = IEnumerable<Complex>;

    record struct BigCoordinate(BigInteger X, BigInteger Y);

    static class Program
    {
        static BigInteger FindExpandedDistances(Input puzzleInput, int expantionRate)
        {
            var (maxX, maxY) = ((int)puzzleInput.Max(c => c.Real) + 1, (int)puzzleInput.Max(c => c.Imaginary) + 1);
            var emptyLines = Enumerable.Range(0, maxY).Where(index => puzzleInput.All(coordinate => coordinate.Imaginary != index));
            var emptyColumns = Enumerable.Range(0, maxX).Where(index => puzzleInput.All(coordinate => coordinate.Real != index));
            var expanded = puzzleInput.Select(coordinate => 
                new BigCoordinate(
                    new BigInteger(coordinate.Real + emptyColumns.Count(column => column < coordinate.Real) * expantionRate),
                    new BigInteger(coordinate.Imaginary + emptyLines.Count(line => line < coordinate.Imaginary) * expantionRate))).ToArray();
            BigInteger lengthSum = 0;
            for (var firstIndex = 0; firstIndex < expanded.Length - 1; firstIndex++)
                for (var secondIndex = firstIndex + 1; secondIndex < expanded.Length; secondIndex++)
                {
                    var first = expanded[firstIndex];
                    var second = expanded[secondIndex];
                    lengthSum += BigInteger.Abs(first.X - second.X) + BigInteger.Abs(first.Y - second.Y); 
                }
            return lengthSum;
        }

        static (BigInteger, BigInteger) Solve(Input puzzleInput)
            => (FindExpandedDistances(puzzleInput, 1), FindExpandedDistances(puzzleInput, 1_000_000 - 1));

        static Input GetInput(string filePath)
        {
            if(!File.Exists(filePath))
                throw new FileNotFoundException(filePath);
            var result = new List<Complex>();
            var y = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                var x = 0;
                foreach (var c in line)
                {
                    if (c == '#')
                        result.Add(new Complex(x, y));
                    x++;
                }
                y++;
            }
            return result;
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
