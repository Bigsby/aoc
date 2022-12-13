using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace AoC
{
    using Input = IEnumerable<Packet>;

    abstract record Packet;
    record NumberPacket(int Value) : Packet;
    record ListPacket(Packet[] Packets) : Packet;

    static class Program
    {
        class PacketComparer : IComparer<Packet>
        {
            private Func<Packet, Packet, bool?> compareFunc;

            public PacketComparer(Func<Packet, Packet, bool?> compareFunc)
                => this.compareFunc = compareFunc;
            
            public int Compare(Packet left, Packet right)
                => compareFunc(left, right) == true ? -1 : 1;
        }

        static bool? AreInOrder(Packet left, Packet right)
        {
            if (left.GetType() != right.GetType())
            {
                if (left is NumberPacket number)
                    return AreInOrder(new ListPacket(new[] { new NumberPacket(number.Value) }), right);
                else
                    return AreInOrder(left, new ListPacket(new[] { new NumberPacket((right as NumberPacket).Value) }));
            }
            if (left is NumberPacket leftNumber && right is NumberPacket rightNumber)
            {
                if (leftNumber.Value == rightNumber.Value)
                    return null;
                return leftNumber.Value < rightNumber.Value;
            }
            var leftList = (left as ListPacket).Packets;
            var rightList = (right as ListPacket).Packets;
            foreach (var (innerLeft, innerRight) in leftList.Zip(rightList, (first, second) => (first, second)))
            {
                var innerInOrder = AreInOrder(innerLeft, innerRight);
                if (innerInOrder.HasValue)
                    return innerInOrder.Value;
            }
            if (leftList.Count() != rightList.Count())
                return leftList.Count() < rightList.Count();
            return null;
        }


        static int Part1(Input packets)
        {
            var orderedSum = 0;
            for (var index = 0; index < packets.Count() / 2; index++)
                if (AreInOrder(packets.ElementAt(index * 2), packets.ElementAt(index * 2 + 1)) == true)
                    orderedSum += index + 1;
            return orderedSum;
        }

        static int Part2(Input packets)
        {
            var dividerOne = new ListPacket(new[] { new ListPacket(new[] { new NumberPacket(2) }) });
            var dividerTwo = new ListPacket(new[] { new ListPacket(new[] { new NumberPacket(6) }) });
            var allPackets = packets.Concat(new[] {
                dividerOne,
                dividerTwo
            });
            var comparer = new PacketComparer(AreInOrder);
            var orderedPacekts = allPackets.OrderBy(packet => packet, comparer);
            var decodeKey = 1;
            for (var index = 0; index < orderedPacekts.Count(); index++)
                if (orderedPacekts.ElementAt(index) == dividerOne || orderedPacekts.ElementAt(index) == dividerTwo)
                    decodeKey *= index + 1;
            return decodeKey;
        }

        static (int, int) Solve(Input puzzleInput)
            => (Part1(puzzleInput), Part2(puzzleInput));

        static Packet ToPacket(JsonElement element)
            => element.ValueKind == JsonValueKind.Number
            ? new NumberPacket(element.GetInt32())
            : new ListPacket(element.EnumerateArray().Select(ToPacket).ToArray());

        static Input GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Where(line => !string.IsNullOrEmpty(line)).Select(line => ToPacket(JsonSerializer.Deserialize<JsonElement>(line)));

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
