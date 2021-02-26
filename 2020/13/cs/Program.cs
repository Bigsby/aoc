using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    record Bus(long id, long index);

    static class Program
    {
        static long Part1((long timestamp, IEnumerable<Bus> busses) puzzleInput)
        {
            var (timestamp, busses) = puzzleInput;
            var closestAfter = long.MaxValue;
            var closestBus = default(Bus);
            foreach (var bus in busses)
            {
                var timeAfter = (timestamp / bus.id + 1) * bus.id - timestamp;
                if (timeAfter < closestAfter)
                {
                    closestAfter = timeAfter;
                    closestBus = bus;
                }
            }
            return closestAfter * closestBus.id;
        }

        static long ModularMultiplicativeInverse(long a, long b)
        {
            var q = a % b;
            for (int i = 1; i < b; i++)
                if ((q * i) % b == 1)
                    return i;
            return 1;
        }

        static long AbsoluteModulo(long a,long n) => ((a % n) + n) % n;

        static long Part2((long timestamp, IEnumerable<Bus> busses) puzzleInput)
        {
            var (_, busses) = puzzleInput;
            var product = busses.Aggregate(1L, (soFar, bus) => soFar * bus.id);
            var sum = 0L;
            foreach (var bus in busses)
            {
                var currentProduct = product / bus.id;
                sum += AbsoluteModulo(bus.id - bus.index, bus.id) 
                    * currentProduct 
                    * ModularMultiplicativeInverse(currentProduct, bus.id);
            }
            return sum % product;
        }

        static (long, long) Solve((long timestamp, IEnumerable<Bus> busses) puzzleInput)
            => (
                Part1(puzzleInput),
                Part2(puzzleInput)
            );

        static (long timestamp, IEnumerable<Bus> busses) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return (
                long.Parse(lines[0]), 
                lines[1].Split(',').Select((busId, index) => (busId, index))
                    .Where(pair => pair.busId != "x")
                    .Select(pair => new Bus(long.Parse(pair.busId), pair.index)));
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