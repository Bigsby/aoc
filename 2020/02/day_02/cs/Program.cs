using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Text.RegularExpressions;

namespace AoC
{
    using Line = Tuple<int, int, char, string>;

    class Program
    {
        static int CountValid(Line[] lines, Func<Line, bool> validationFunc)
            => lines.Where(validationFunc).Count();

        static int Part1(Line[] lines)
        {
            return CountValid(lines, line => {
                var (minimum, maximum, letter, password) = line;
                var occurenceCount = password.Count(c => c == letter);
                return occurenceCount >= minimum && occurenceCount <= maximum;
            });
        }

        static int Part2(Line[] lines)
        {
            return CountValid(lines, line => {
                var (first, second, letter, password) = line;
                return (password[first - 1] == letter) ^ (password[second  - 1] == letter);
            });
        }

        static Regex lineRegex = new Regex(@"^(\d+)-(\d+)\s([a-z]):\s(.*)$", RegexOptions.Compiled);
        static Line[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return Tuple.Create(
                        int.Parse(match.Groups[1].Value),
                        int.Parse(match.Groups[2].Value),
                        match.Groups[3].Value[0],
                        match.Groups[4].Value
                    );
                throw new Exception("Bad format {line}");
            }).ToArray();
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