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

        static int GetMirrorValue(IEnumerable<Complex> pattern)
        {
            // PrintPattern(pattern);
            var (maxX, maxY) = GetMaxs(pattern);
            var areRowsEqual = (int one, int two) => Enumerable.Range(0, maxX).All(column => !pattern.Contains(new Complex(column, one)) ^ pattern.Contains(new Complex(column, two)));
            var areColumnsEqual = (int one, int two) => Enumerable.Range(0, maxY).All(row => !pattern.Contains(new Complex(one, row)) ^ pattern.Contains(new Complex(two, row)));
            var hasReflection = (int max, Func<int, int, bool> equalityTester, out int reflectionIndex) =>
            {
                for (var index = 0; index < max; index++)
                    if (equalityTester(index, index + 1))
                    {
                        var one = index - 1;
                        var two = index + 2;
                        var isReflection = true;
                        while (one >= 0 && two < max)
                            if (!(isReflection &= equalityTester(one--, two++)))
                                break;
                        reflectionIndex = index + 1; 
                        if (isReflection)
                            return isReflection;
                    }
                reflectionIndex = -1;
                return false;
            };
            if (hasReflection(maxY, areRowsEqual, out var rowIndex))
                return rowIndex * 100;
            if (hasReflection(maxX, areColumnsEqual, out var columnIndex))
                return columnIndex;

            // for (var row = 0; row < maxY - 1; row++)
            // {
            //     if (areRowsEqual(row, row + 1))
            //     {
            //         WriteLine($"Equal rows {row} {row + 1}");
            //         var one = row - 1;
            //         var two = row + 2;
            //         var isReflection = true;
            //         while (one >= 0 && two < maxY)
            //             if (!(isReflection &= areRowsEqual(one--, two++)))
            //                 break;
            //         WriteLine($"Reflection {isReflection} {one} {two}");
            //         if (isReflection)
            //         {
            //             WriteLine($"Row {row}");
            //             return (row + 1) * 100;
            //         }
            //     }
            // }

            // for (var column = 0; column < maxX - 1; column++)
            // {
            //     if (areColumnsEqual(column, column + 1))
            //     {
            //         WriteLine($"Equal columns {column} {column + 1}");
            //         var one = column - 1;
            //         var two = column + 2;
            //         var isReflection = true;
            //         while (one >= 0 && two < maxX)
            //             if (!(isReflection &= areColumnsEqual(one--, two++)))
            //                 break;
            //         WriteLine($"Reflection {isReflection} {one} {two}");
            //         if (isReflection)
            //         {
            //             WriteLine($"Column {column}");
            //             return column + 1;
            //         }
            //     }
            // }
            throw new Exception("Reflection not found!");
        }
        
        static int Part1(Input puzzleInput)
        { 
            return puzzleInput.Sum(pattern => GetMirrorValue(pattern));
        }

        static int Part2(Input puzzleInput)
        {
            return 2;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

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
