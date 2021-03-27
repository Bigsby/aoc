using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Operation = Tuple<int, int, int, int>;
    using Registers = Tuple<int, int, int, int>;

    static class Program
    {
        static string[] MNEMONICS = new[] {
            "addr", "addi",
            "mulr", "muli",
            "banr", "bani",
            "borr", "bori",
            "setr", "seti",
            "gtir", "gtri", "gtrr",
            "eqir", "eqri", "eqrr"
        };

        static Registers RunOperation(Registers registers, Operation operation, string mnemonic)
        {
            var (_, a, b, c) = operation;
            var result = new[] { registers.Item1, registers.Item2, registers.Item3, registers.Item4 };
            result[c] = mnemonic switch
            {
                "addr" => result[a] + result[b],
                "addi" => result[a] + b,
                "mulr" => result[a] * result[b],
                "muli" => result[a] * b,
                "banr" => result[a] & result[b],
                "bani" => result[a] & b,
                "borr" => result[a] | result[b],
                "bori" => result[a] | b,
                "setr" => result[a],
                "seti" => a,
                "gtir" => a > result[b] ? 1 : 0,
                "gtri" => result[a] > b ? 1 : 0,
                "gtrr" => result[a] > result[b] ? 1 : 0,
                "eqir" => a == result[b] ? 1 : 0,
                "eqri" => result[a] == b ? 1 : 0,
                "eqrr" => result[a] == result[b] ? 1 : 0,
                _ => throw new Exception($"Uknow mnemonic '{mnemonic}'")
            };
            return Tuple.Create(result[0], result[1], result[2], result[3]);
        }

        static bool AreEqual(Registers a, Registers b)
            => a.Item1 == b.Item1 && a.Item2 == b.Item2 && a.Item3 == b.Item3 && a.Item4 == b.Item4;

        static int TestRecord(Registers before, Operation operation, Registers after, Dictionary<string, HashSet<int>> opCodes)
        {
            var count = 0;
            var (opCode, _, _, _) = operation;
            foreach (var mnenomic in MNEMONICS)
            {
                if (AreEqual(after, RunOperation(before, operation, mnenomic)))
                {
                    if (!opCodes[mnenomic].Contains(-opCode))
                        opCodes[mnenomic].Add(opCode);
                    count++;
                }
                else if (opCodes[mnenomic].Contains(opCode))
                {
                    opCodes[mnenomic].Remove(opCode);
                    opCodes[mnenomic].Add(-opCode);
                }
            }
            return count;
        }

        static (int, int) Solve((IEnumerable<(Registers before, Operation operation, Registers after)> records, IEnumerable<Operation> operations) puzzleInput)
        {
            var (records, program) = puzzleInput;
            var opCodes = MNEMONICS.ToDictionary(mnemonic => mnemonic, _ => new HashSet<int>());
            var threeOrMore = 0;
            foreach (var (before, operation, after) in records)
                if (TestRecord(before, operation, after, opCodes) > 2)
                    threeOrMore++;
            foreach (var mnemonic in opCodes.Keys.ToArray())
                opCodes[mnemonic] = opCodes[mnemonic].Where(opCode => opCode >= 0).ToHashSet();
            while (opCodes.Values.Any(valid => valid.Count > 1))
            {
                var singleValid = opCodes.Values.Where(valid => valid.Count == 1).Select(valid => valid.First()).ToArray();
                foreach (var pair in opCodes)
                    if (pair.Value.Count > 1)
                        foreach (var single in singleValid)
                            pair.Value.Remove(single);
            }
            var ops = opCodes.ToDictionary(pair => pair.Value.Single(), pair => pair.Key);
            var registers = Tuple.Create(0, 0, 0, 0);
            foreach (var operation in program)
                registers = RunOperation(registers, operation, ops[operation.Item1]);
            return (threeOrMore, registers.Item1);
        }

        static Regex recordRegex = new Regex(@"Before: \[(?<b0>\d+), (?<b1>\d+), (?<b2>\d+), (?<b3>\d+)][^\d]*(?<opCode>\d+) (?<A>\d+) (?<B>\d+) (?<C>\d+).*After:  \[(?<a0>\d+), (?<a1>\d+), (?<a2>\d+), (?<a3>\d+)]", RegexOptions.Compiled | RegexOptions.Singleline);
        static Regex operationRegex = new Regex(@"(?<opCode>\d+) (?<A>\d) (?<B>\d) (?<C>\d)", RegexOptions.Compiled);
        static (IEnumerable<(Registers before, Operation operation, Registers after)> records, IEnumerable<Operation> operations) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var splits = File.ReadAllText(filePath).Split(Environment.NewLine + Environment.NewLine + Environment.NewLine + Environment.NewLine);
            var records = new List<(Registers before, Operation operation, Registers after)>();
            foreach (Match match in splits[0].Split(Environment.NewLine + Environment.NewLine).Select(record => recordRegex.Match(record)))
                records.Add((
                    Tuple.Create(int.Parse(match.Groups["b0"].Value), int.Parse(match.Groups["b1"].Value), int.Parse(match.Groups["b2"].Value), int.Parse(match.Groups["b3"].Value)),
                    Tuple.Create(int.Parse(match.Groups["opCode"].Value), int.Parse(match.Groups["A"].Value), int.Parse(match.Groups["B"].Value), int.Parse(match.Groups["C"].Value)),
                    Tuple.Create(int.Parse(match.Groups["a0"].Value), int.Parse(match.Groups["a1"].Value), int.Parse(match.Groups["a2"].Value), int.Parse(match.Groups["a3"].Value))
                ));

            var operations = new List<Operation>();
            foreach (Match match in operationRegex.Matches(splits[1]))
                operations.Add(Tuple.Create(int.Parse(match.Groups["opCode"].Value), int.Parse(match.Groups["A"].Value), int.Parse(match.Groups["B"].Value), int.Parse(match.Groups["C"].Value)));
            return (records, operations);
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