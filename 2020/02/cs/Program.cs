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

        static (int, int) Solve(Line[] lines)
            => (
                CountValid(lines, line => {
                    var (minimum, maximum, letter, password) = line;
                    var occurenceCount = password.Count(c => c == letter);
                    return occurenceCount >= minimum && occurenceCount <= maximum;
                }),
                CountValid(lines, line => {
                    var (first, second, letter, password) = line;
                    return (password[first - 1] == letter) ^ (password[second  - 1] == letter);
                })
            );

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