using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Numerics;

namespace AoC
{
    using Input = Tuple<IEnumerable<Complex>, IEnumerable<Complex>>;

    static class Program
    {
        static void DisplayDish(Input rocks)
        {
            var (rounded, cubed) = rocks;
            var maxX = Math.Max(rounded.Max(c => c.Real), cubed.Max(c => c.Real)) + 1;
            var maxY = Math.Max(rounded.Max(c => c.Imaginary), cubed.Max(c => c.Imaginary)) + 1;
            for (var row = 0; row < maxY; row++)
            {
                for (var column = 0; column < maxX; column++)
                {
                    var c = '.';
                    var rock = new Complex(column, row);
                    if (rounded.Contains(rock))
                        c = 'O';
                    else if (cubed.Contains(rock))
                        c = '#';
                    Write(c);
                }
                WriteLine();
            }
            WriteLine();
        }

        static int Part1(Input puzzleInput)
        { 
            DisplayDish(puzzleInput);
            var (rounded, cubed) = puzzleInput;
            var newRounded = new List<Complex>();
            foreach (var rock in rounded.OrderBy(r => r.Imaginary))
            {
                var (x, y) = ((int)rock.Real, (int)rock.Imaginary);
                while (true)
                {
                    y--;
                    var newPosition = new Complex(x, y);
                    if (cubed.Contains(newPosition) || newRounded.Contains(newPosition) || y == -1)
                    {
                        newRounded.Add(new Complex(x, y + 1));
                        break;
                    }
                }
            }
            DisplayDish(Tuple.Create<IEnumerable<Complex>, IEnumerable<Complex>>(newRounded, cubed));
            var maxLoad = (int)cubed.Max(rock => rock.Imaginary) + 1;
            return newRounded.Sum(rock => maxLoad - (int)rock.Imaginary);
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
            var rounded = new List<Complex>();
            var cubed = new List<Complex>();
            var row = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                var column = 0;
                foreach (var c in line)
                {
                    switch (c)
                    {
                        case 'O':
                            rounded.Add(new Complex(column, row));
                            break;
                        case '#':
                            cubed.Add(new Complex(column, row));
                            break;
                    }
                    column++;
                }
                row++;
            }

            return Tuple.Create<IEnumerable<Complex>, IEnumerable<Complex>>(rounded, cubed);
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
