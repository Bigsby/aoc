using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class AuntRecord
    {
        public const int NA_PROP = -1;
        public int Number { get; }
        public Dictionary<string, int> Properties { get; } = PROPS.ToDictionary(prop => prop, prop => NA_PROP);

        public AuntRecord(string number,
            string prop1Name, string prop1Value,
            string prop2Name, string prop2Value,
            string prop3Name, string prop3Value)
        {
            Number = int.Parse(number);
            Properties[prop1Name] = int.Parse(prop1Value);
            Properties[prop2Name] = int.Parse(prop2Value);
            Properties[prop3Name] = int.Parse(prop3Value);
        }

        static string[] PROPS = new [] { 
            "children", "cats", "samoyeds", "pomeranians", "akitas", "vizslas", "goldfish", "trees", "cars", "perfumes" };
    }

    enum Operator
    {
        EQUAL,
        GREATER,
        LESS
    }

    record Reading(int value, Operator oper = Operator.EQUAL);

    static class Program
    {
        static Dictionary<string, Reading> MFCSAN_READING = new Dictionary<string, Reading> {
            { "children", new Reading(3) },
            { "cats", new Reading(7, Operator.GREATER) },
            { "samoyeds", new Reading(2) },
            { "pomeranians", new Reading(3, Operator.LESS) },
            { "akitas", new Reading(0) },
            { "vizslas", new Reading(0) },
            { "goldfish", new Reading(5, Operator.LESS) },
            { "trees", new Reading(5, Operator.GREATER) },
            { "cars", new Reading(2) },
            { "perfumes", new Reading(1) }
        };
        static bool IsValidRecord(AuntRecord record, bool checkOperator = false)
        {
            foreach (var prop in MFCSAN_READING.Keys)
            {
                var recordValue = record.Properties[prop];
                if (recordValue == AuntRecord.NA_PROP)
                    continue;
                var reading = MFCSAN_READING[prop];
                var readingValue = reading.value;
                if (checkOperator)
                {
                    if ((reading.oper == Operator.EQUAL && recordValue != readingValue)
                        || (reading.oper == Operator.GREATER && recordValue <= readingValue)
                        || (reading.oper == Operator.LESS && recordValue >= readingValue))
                        return false;
                }
                else if (recordValue != readingValue)
                    return false;
            }
            return true;
        }

        static (int, int) Solve(IEnumerable<AuntRecord> aunts)
            => (
                aunts.First(record => IsValidRecord(record)).Number, 
                aunts.First(record => IsValidRecord(record, true)).Number
            );

        static Regex lineRegex = new Regex(@"^Sue\s(\d+):\s(\w+):\s(\d+),\s(\w+):\s(\d+),\s(\w+):\s(\d+)$", RegexOptions.Compiled);
        static IEnumerable<AuntRecord> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new AuntRecord(
                        match.Groups[1].Value,
                        match.Groups[2].Value,
                        match.Groups[3].Value,
                        match.Groups[4].Value,
                        match.Groups[5].Value,
                        match.Groups[6].Value,
                        match.Groups[7].Value
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