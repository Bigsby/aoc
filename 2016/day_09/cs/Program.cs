using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        static Regex markerRegex = new Regex(@"(?<prior>[A-Z]*)\((?<length>\d+)x(?<repeats>\d+)\)(?<data>.*)", RegexOptions.Compiled);
        static long GetLength(string data, bool recursive)
        {
            var match = markerRegex.Match(data);
            if (match.Success)
            {
                var dataLength = int.Parse(match.Groups["length"].Value);
                data = match.Groups["data"].Value;
                return match.Groups["prior"].Length 
                    + int.Parse(match.Groups["repeats"].Value) 
                    * (recursive ? GetLength(data[Range.EndAt(dataLength)], true) : dataLength)
                    + GetLength(data[Range.StartAt(dataLength)], recursive);
            }
            else
                return data.Length;
        }

        static long Part1(string data) => GetLength(data, false);

        static long Part2(string data) => GetLength(data, true);

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