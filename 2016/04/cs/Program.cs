using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using System.Text;

namespace AoC
{
    using Rooms = IEnumerable<(string name, int id, string checksum)>;
    class Program
    {
        static bool IsRoomValid(string name, string checksum)
        {
            name = name.Replace("-", "");
            var counts = name.Distinct().ToDictionary(c => c, c => name.Count(t => t == c));
            var processedChecksum = string.Join("", counts.OrderBy(kv => -kv.Value * 100 + kv.Key).Take(5).Select(kv=> kv.Key));
            return processedChecksum == checksum;
        }

        const byte A_ORD = (byte)'a';
        const byte Z_ORD = (byte)'z';
        const byte DASH_ORD = (byte)'-';
        const byte SPACE_ORD = (byte)' ';
        static byte GetNextChar(byte c)
        {
            if (c == DASH_ORD || c == SPACE_ORD) return SPACE_ORD;
            if (c == Z_ORD) return A_ORD;
            else return ++c;
        }

        static string RotateName(string name, int count)
        {
            var nameBytes = UTF32Encoding.UTF8.GetBytes(name);
            foreach (var _ in Enumerable.Range(0, count))
                foreach (var index in Enumerable.Range(0, nameBytes.Length))
                    nameBytes[index] = GetNextChar(nameBytes[index]);
            return UTF8Encoding.UTF8.GetString(nameBytes);
        }

        const string SEARCH_NAME = "northpole object storage";
        static int Part2(Rooms rooms)
        {
            foreach (var (name, id, checksum) in rooms)
                if (IsRoomValid(name, checksum) && RotateName(name, id) == SEARCH_NAME)
                    return id;
            throw new Exception("Room not found");
        }

        static (int, int) Solve(Rooms rooms)
            => (
                rooms.Where(room => IsRoomValid(room.name, room.checksum)).Sum(room => room.id), 
                Part2(rooms)
            );

        static Regex lineRegex = new Regex(@"^(?<name>[a-z\-]+)-(?<id>\d+)\[(?<checksum>\w+)\]$");
        static Rooms GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return (
                        match.Groups["name"].Value,
                        int.Parse(match.Groups["id"].Value),
                        match.Groups["checksum"].Value
                    );
                throw new Exception($"Bad format '{line}'");
            });

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