using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = IEnumerable<IEnumerable<Complex>>;

    static class Program
    {
        static (int, int) GetMaxs(IEnumerable<Complex> pattern)
            => ((int)pattern.Max(c => c.Real) + 1, (int)pattern.Max(c => c.Imaginary) + 1);
        
        static void PrintPattern(IEnumerable<Complex> pattern)
        {
            var (maxX, maxY) = GetMaxs(pattern);
            for (var row = 0; row < maxY; row++)
            {
                for (var column = 0; column < maxX; column++)
                    Write(pattern.Contains(new Complex(column, row)) ? '#' : '.');
                WriteLine();
            }
        }
        
        static void PrintPatterns(Input patterns)
        {
            foreach (var pattern in patterns)
            {
                PrintPattern(pattern);
                WriteLine();
            }
        }

        static int GetMirrorValue(IEnumerable<Complex> pattern, int maximumDifference = 0)
        {
            PrintPattern(pattern);
            var (maxX, maxY) = GetMaxs(pattern);
            var rowDifferenceCounter = (int one, int two) 
                => Enumerable.Range(0, maxX)
                    .Count(column => pattern.Contains(new Complex(column, one)) ^ pattern.Contains(new Complex(column, two)));
            var columnDifferenceCounter = (int one, int two) 
                => Enumerable.Range(0, maxY)
                    .Count(row => pattern.Contains(new Complex(one, row)) ^ pattern.Contains(new Complex(two, row)));
            var hasReflection = (int max, Func<int, int, int> differenceCounter, string name, out int reflectionIndex) =>
            {
                for (var index = 0; index < max; index++)
                {
                    var differences = 0;
                    if ((differences = differenceCounter(index, index + 1)) <= maximumDifference)
                    {
                        var one = index - 1;
                        var two = index + 2;
                        while (one >= 0 && two < max && differences <= maximumDifference)
                            differences += differenceCounter(one--, two++);
                        if (differences <= maximumDifference)
                        {
                            reflectionIndex = index + 1; 
                            // WriteLine($"{name} {reflectionIndex} {maximumDifference} {one} {two}"); ReadLine();
                            return true;
                        }
                    }
                }
                reflectionIndex = -1;
                return false;
            };
            if (hasReflection(maxY, rowDifferenceCounter, "row", out var rowIndex))
                return rowIndex * 100;
            if (hasReflection(maxX, columnDifferenceCounter, "column", out var columnIndex))
                return columnIndex;
                
            throw new Exception("Reflection not found!");
        }
        
        static int Part2(Input puzzleInput)
        {
            return 2;
        }

        static (int, int) Solve(Input puzzleInput)
            => (puzzleInput.Sum(pattern => GetMirrorValue(pattern)), puzzleInput.Sum(pattern => GetMirrorValue(pattern, 1)));

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) 
                throw new FileNotFoundException(filePath);
            
            var result = new List<IEnumerable<Complex>>();
            var pattern = new List<Complex>();
            var row = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (string.IsNullOrEmpty(line))
                {
                    result.Add(pattern);
                    pattern = new List<Complex>();
                    row = 0;
                }
                else 
                {
                    var column = 0;
                    foreach (var c in line.Trim())
                    {
                        if (c == '#')
                            pattern.Add(new Complex(column, row));
                        column++;
                    }
                    row++;
                }
            }
            result.Add(pattern);
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
