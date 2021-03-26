using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Instruction = Tuple<int, int, int>;

    static class Program
    {
        static List<int> ToOrd(string programs) => programs.Select(c => (int)c).ToList();

        static string ToString(IEnumerable<int> programs) => new string(programs.Select(c => (char)c).ToArray());

        static List<int> Dance(IEnumerable<Instruction> instructions, List<int> programs)
        {
            foreach (var (move, a, b) in instructions)
            {
                if (move == 0)
                {
                    var index = programs.Count() - a;
                    programs = programs.Skip(index).Concat(programs.Take(index)).ToList();
                }
                else if (move == 1)
                {
                    var oldA = programs[a];
                    programs[a] = programs[b];
                    programs[b] = oldA;
                }
                else if (move == 2)
                {
                    var aIndex = programs.IndexOf(a);
                    var bIndex = programs.IndexOf(b);
                    var oldA = programs[aIndex];
                    programs[aIndex] = programs[bIndex];
                    programs[bIndex] = oldA;
                }
            }
            return programs.ToList();
        }

        const int CYCLES = 1_000_000_000;
        static string Part2(IEnumerable<Instruction> instructions)
        {
            var programs = ToOrd("abcdefghijklmnop");
            var seen = new List<string>();
            seen.Add(ToString(programs));
            for (var cycle = 0; cycle < CYCLES; cycle++)
            {
                programs = Dance(instructions, programs);
                var pString = ToString(programs);
                if (seen.Contains(pString))
                    return seen.ElementAt(CYCLES % (cycle + 1));
                seen.Add(pString);
            }
            return ToString(programs);
        }

        static (string, string) Solve(IEnumerable<Instruction> instructions)
            => (
                ToString(Dance(instructions, ToOrd("abcdefghijklmnop"))),
                Part2(instructions)
            );

        static Instruction[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Split(',').Select(text =>
            {
                if (text.StartsWith("s"))
                    return Tuple.Create(0, int.Parse(text[1..]), 0);
                else if (text.StartsWith("x"))
                {
                    var splits = text[1..].Split('/');
                    return Tuple.Create(1, int.Parse(splits[0]), int.Parse(splits[1]));
                }
                else if (text.StartsWith("p"))
                {
                    var splits = text[1..].Split('/');
                    return Tuple.Create(2, (int)splits[0][0], (int)splits[1][0]);
                }
                throw new Exception($"Unknow instruction '{text}'");
            }).ToArray();

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