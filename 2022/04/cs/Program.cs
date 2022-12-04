using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<Tuple<int, int, int, int>>;

    static class Program
    {

        static bool HasContainer(Tuple<int, int, int, int> pair)
        => pair.Item3 >= pair.Item1 && pair.Item4 <= pair.Item2
        || pair.Item1 >= pair.Item3 && pair.Item2 <= pair.Item4;

        static bool ContainsOverlap(Tuple<int, int, int, int> pair)
        => (pair.Item3 <= pair.Item1 && pair.Item1 <= pair.Item4)
        || (pair.Item3 <= pair.Item2 && pair.Item2 <= pair.Item4)
        || (pair.Item1 <= pair.Item3 && pair.Item3 <= pair.Item2)
        || (pair.Item1 <= pair.Item4 && pair.Item4 <= pair.Item2);

        static (int, int) Solve(Input pairs)
            => (pairs.Count(HasContainer), pairs.Count(ContainsOverlap));

        static Tuple<int, int, int, int> ProcessLine(string line)
        {
            var pair = line.Split(',');
            var first = pair[0].Split('-');
            var second = pair[1].Split('-');
            return Tuple.Create(
                int.Parse(first[0]),
                int.Parse(first[1]),
                int.Parse(second[0]),
                int.Parse(second[1]));
        }

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(ProcessLine);

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
