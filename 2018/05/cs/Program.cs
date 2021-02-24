using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static int Part1(string polymer)
        {
            var polymerBytes = polymer.Select(c => (byte)c).ToList();
            var hadChanges = true;
            while (hadChanges)
            {
                hadChanges = false;
                var index = 0;
                while (index < polymerBytes.Count - 1)
                    if (Math.Abs(polymerBytes[index] - polymerBytes[index + 1]) == 32)
                    {
                        polymerBytes.RemoveAt(index);
                        polymerBytes.RemoveAt(index);
                        hadChanges = true;
                    }
                    else
                        index++;
            }
            return polymerBytes.Count;
        }

        static int Part2(string polymer)
        {
            var minUnits = int.MaxValue;
            foreach(var cByte in Enumerable.Range((int)'A', (int)'Z' - (int)'A' + 1))
            {
                var strippedPolymer = Regex.Replace(polymer, "[" + (char)cByte + (char)(cByte + 32) + "]", "");
                minUnits = Math.Min(minUnits, Part1(strippedPolymer));
            }
            return minUnits;
        }

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