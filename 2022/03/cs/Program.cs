using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<string>;

    static class Program
    {
        static int GetItemPriority(char item)
        => (item < 'a' ? item - 'A' + 26 : item - 'a') + 1;

        static int GetRepeatedItemPriority(string rucksack)
        {
            var cut = rucksack.Length / 2;
            var first = rucksack.Substring(0, cut);
            var second = rucksack.Substring(cut);
            foreach (var item in first)
                if (second.Contains(item))
                    return GetItemPriority(item);
            throw new Exception("Repeated item not found!");
        }

        static int Part1(Input rucksacks)
        => rucksacks.Sum(rucksack => GetRepeatedItemPriority(rucksack));

        static int Part2(Input rucksacks)
        {
            var total = 0;
            for (var index = 0; index < rucksacks.Count() / 3; index++)
            {
                var first = rucksacks.ElementAt(index * 3);
                var second = rucksacks.ElementAt(index * 3 + 1);
                var third = rucksacks.ElementAt(index * 3 + 2);
                foreach (var item in first)
                    if (second.Contains(item) && third.Contains(item))
                    {
                        total += GetItemPriority(item);
                        break;
                    }
            }
            return total;
        }

        static (int, int) Solve(Input rucksacks)
            => (Part1(rucksacks), Part2(rucksacks));

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath);

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
