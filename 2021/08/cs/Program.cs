using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class Connection
    {
        public Connection(int[] wires, int[] displays)
        {
            Wires = wires;
            Displays = displays;
        }
        public int[] Wires { get; private set; }
        public int[] Displays { get; private set; }
    }
    
    static class Program
    {
        static int GetBitCount(int wire)
        {
            var count = 0;
            while (wire != 0)
            {
                if ((wire & 1) == 1)
                    count++;
                wire >>= 1;
            }
            return count;
        }

        static int Part1(IEnumerable<Connection> connections)
        { 
            var bitCounts = new [] { 2, 3, 4, 7 };
            return connections.Sum(connection => connection.Displays.Count(display => bitCounts.Contains(GetBitCount(display))));
        }

        static void FilterAndRemove(Connection connection, int[] digits, int digit, int digitLenght, int exceptDigit, int exceptLength)
        {
            for (var wire = 0; wire < 10; wire++)
            {
                var segments = connection.Wires[wire];
                if (segments == 0)
                    continue;
                var length = GetBitCount(segments);
                if (length == digitLenght && (exceptLength == 0 || GetBitCount(segments & ~digits[exceptDigit]) == exceptLength))
                {
                    digits[digit] = segments;
                    connection.Wires[wire] = 0;
                    return;
                }
            }
        }

        static int GetConnectionValue(Connection connection)
        {
            var digits = new int[10];
            FilterAndRemove(connection, digits, 7, 3, 0, 0);
            FilterAndRemove(connection, digits, 4, 4, 0, 0);
            FilterAndRemove(connection, digits, 1, 2, 0, 0);
            FilterAndRemove(connection, digits, 8, 7, 0, 0);
            FilterAndRemove(connection, digits, 3, 5, 1, 3);
            FilterAndRemove(connection, digits, 6, 6, 1, 5);
            FilterAndRemove(connection, digits, 2, 5, 4, 3);
            FilterAndRemove(connection, digits, 5, 5, 4, 2);
            FilterAndRemove(connection, digits, 0, 6, 4, 3);
            digits[9] = connection.Wires.First(wire => wire != 0);
            var decode = digits.Select((segments, index) => new { segments, index })
                .ToDictionary(pair => pair.segments, pair => pair.index);
            var total = 0;
            for (int displayIndex = 0; displayIndex < 4; displayIndex++)
                total += decode[connection.Displays[displayIndex]] * (int)Math.Pow(10, 3 - displayIndex);
            return total;
        }

        static int Part2(IEnumerable<Connection> connections)
            => connections.Sum(connection => GetConnectionValue(connection));

        static (int, int) Solve(IEnumerable<Connection> connections)
            => (Part1(connections), Part2(connections));

        static int ParseWire(string wire)
            => wire.Aggregate(0, (soFar, segment) => soFar | (1 << ((int)segment - (int)'a')));

        static IEnumerable<Connection> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => {
                var split = line.Split(" | ");
                return new Connection(
                    split[0].Split(" ").Select(ParseWire).ToArray(),
                    split[1].Split(" ").Select(ParseWire).ToArray()
                    );
            });
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
