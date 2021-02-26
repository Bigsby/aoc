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

        static (long, long) Solve(string data)
            => (
                GetLength(data, false), 
                GetLength(data, true)
            );

        static string GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim();

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