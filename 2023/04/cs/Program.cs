using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<(int, IEnumerable<int>, IEnumerable<int>)>;

    static class Program
    {
        static (int, int) Solve(Input cards)
        {
            var part1 = 0;
            var won = cards.Select(_ => 1).ToArray();
            foreach (var (card, index) in cards.Select((c, i) => (c, i)))
            {
                var (number, winning, own) = card;
                var matches = winning.Count(number => own.Contains(number));
                if (matches > 0)
                    part1 += (int)Math.Pow(2, matches - 1);
                for (var offset = 0; offset < matches; offset++)
                    won[index + offset + 1] += won[index];
            }
            return (part1, won.Sum());
        }
        
        static (int, IEnumerable<int>, IEnumerable<int>) ParseCard(string line)
        {
            var lineSplit = line.Split(":");
            var (header, numbers) = (lineSplit[0], lineSplit[1]);
            var numberSplit = numbers.Trim().Split("|");
            var (winning, own) = (numberSplit[0], numberSplit[1]);
            return (
                int.Parse(header.Split(" ")[^1]),
                winning.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(value => int.Parse(value.Trim())),
                own.Split(" ", StringSplitOptions.RemoveEmptyEntries).Select(value => int.Parse(value.Trim())));
        }

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => ParseCard(line.Trim()));

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
