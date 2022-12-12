using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Input = IEnumerable<Monkey>;

    class Monkey
    {
        public Monkey(List<long> items, Func<long, long> operation, long test, int throwTrue, int throwFalse)
        {
            Items = items;
            Operation = operation;
            Test = test;
            ThrowTrue = throwTrue;
            ThrowFalse = throwFalse;
            Inspections = 0;
        }

        public List<long> Items { get; init; }
        public Func<long, long> Operation { get; init; }
        public long Test { get; init; }
        public int ThrowTrue { get; init; }
        public int ThrowFalse { get; init; }
        public long Inspections { get; set; }

        public Monkey Clone()
        {
            return new Monkey(
                new List<long>(Items),
                Operation,
                Test,
                ThrowTrue,
                ThrowFalse
            );
        }
    }

    static class Program
    {
        static long DoRounds(Input initialMonkeys, int worryLevel, int rounds, long commonDivider)
        {
            var monkeys = initialMonkeys.Select(monkey => monkey.Clone()).ToArray();
            var divide = commonDivider != 1;
            for (var round = 0; round < rounds; round++)
                foreach (var monkey in monkeys)
                {
                    foreach (var initialItem in monkey.Items)
                    {
                        var item = monkey.Operation(initialItem) / worryLevel;
                        if (divide)
                            item %= commonDivider;
                        monkeys[item % monkey.Test == 0 ? monkey.ThrowTrue : monkey.ThrowFalse].Items.Add(item);
                        monkey.Inspections++;
                    }
                    monkey.Items.Clear();
                }
            var inspections = monkeys.Select(monkey => monkey.Inspections).OrderByDescending(i => i).ToArray();
            return inspections[0] * inspections[1];
        }

        static (long, long) Solve(Input monkeys)
            => (DoRounds(monkeys, 3, 20, 1), DoRounds(monkeys, 1, 10_000, monkeys.Aggregate(1L, (soFar, monkey) => soFar * monkey.Test)));

        static Func<long, long> ParseOperation(string text)
        {
            var split = text.Split(' ');
            var value = split[2] == "old" ? 0 : long.Parse(split[2]);
            if (split[1] == "*")
                return value == 0 ?
                    old => old * old
                    :
                    old => old * value;
            return value == 0 ?
                    old => old + old
                    :
                    old => old + value;
        }

        static Input GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var monkeys = new List<Monkey>();
            var items = new List<long>();
            Func<long, long> operation = x => throw new NotImplementedException();
            long test = 0;
            int throwTrue = 0, throwFalse = 0;
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (line.StartsWith("  Starting items:"))
                    items = new List<long>(line.Split(':')[1].Trim().Split(", ").Select(item => long.Parse(item)));
                else if (line.StartsWith("  Operation:"))
                    operation = ParseOperation(line.Split(':')[1].Trim().Split(" = ")[1].Trim());
                else if (line.StartsWith("  Test:"))
                    test = long.Parse(line.Split(" ").Last());
                else if (line.StartsWith("    If true:"))
                    throwTrue = int.Parse(line.Split(' ').Last());
                else if (line.StartsWith("    If false:"))
                {
                    throwFalse = int.Parse(line.Split(' ').Last());
                    monkeys.Add(new Monkey(items, operation, test, throwTrue, throwFalse));
                }
            }
            return monkeys;
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
