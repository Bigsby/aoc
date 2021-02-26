using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Operation = Tuple<string, int, int, int>;

    static class Program
    {
        const int MASK = 16777215;
        const int MULTIPLIER = 65899;
        static (int, int) Solve((int, Operation[] operations) data)
        {
            var magicNumber = data.operations[7].Item2;
            var part1Result = 0;
            var seen = new HashSet<int>();
            var result = 0;
            var lastResult = -1;
            while (true)
            {
                var accumulator = result | 0x10000;
                result = magicNumber;
                while (true)
                {
                    result = (((result + (accumulator & 0xFF)) & MASK) * MULTIPLIER) & MASK;
                    if (accumulator <= 0xFF)
                    {
                        if (part1Result == 0)
                            part1Result = result;
                        if (!seen.Contains(result))
                        {
                            seen.Add(result);
                            lastResult = result;
                            break;
                        }
                        else
                            return (part1Result, lastResult);
                    }
                    else
                        accumulator /= 0x100;
                }
            }
        }

        static Regex operationRegex = new Regex(@"(?<opCode>\w+) (?<A>\d+) (?<B>\d+) (?<C>\d+)", RegexOptions.Compiled);
        static (int, Operation[] operations) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return (int.Parse(lines[0].Split(" ")[1]), lines[1..].Select(line => {
                var match = operationRegex.Match(line);
                if (match.Success)
                    return Tuple.Create(match.Groups["opCode"].Value, int.Parse(match.Groups["A"].Value), int.Parse(match.Groups["B"].Value), int.Parse(match.Groups["C"].Value));
                throw new Exception($"Bad format '{line}'");
            }).ToArray());
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
