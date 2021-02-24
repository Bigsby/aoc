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
        static int Part1(int[][] lines)
        {
            return lines.Select(line => line.Max() - line.Min()).Sum();
        }

        static int Part2(int[][] lines)
        {
            var total = 0;
            foreach (var line in lines)
            {
                foreach (var numberA in line)
                {
                    foreach(var numberB in line)
                    {
                        if (numberA > numberB && numberA % numberB == 0)
                        {
                            total += numberA / numberB;
                        }
                    }
                }
            }
            return total;
        }

        static Regex lineRegex = new Regex(@"\d+", RegexOptions.Compiled);
        static int[][] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath)
                .Select(line => 
                lineRegex.Matches(line).Select(match => int.Parse(match.Groups[0].Value)).ToArray()).ToArray();
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