﻿using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Operation = Tuple<string, int, int, int>;

    static class Program
    {
        static int[] RunOperation(int[] registers, Operation operation)
        {
            var (mnemonic, A, B, C) = operation;
            registers = registers.ToArray();
            var value = -1;
            switch (mnemonic)
            {
                case "addr": value = registers[A] + registers[B]; break;
                case "addi": value = registers[A] + B; break;
                case "mulr": value = registers[A] * registers[B]; break;
                case "muli": value = registers[A] * B; break;
                case "banr": value = registers[A] & registers[B]; break;
                case "bani": value = registers[A] & B; break;
                case "borr": value = registers[A] | registers[B]; break;
                case "bori": value = registers[A] | B; break;
                case "setr": value = registers[A]; break;
                case "seti": value = A; break;
                case "gtir": value = A > registers[B] ? 1 : 0; break;
                case "gtri": value = registers[A] > B ? 1 : 0; break;
                case "gtrr": value = registers[A] > registers[B] ? 1 : 0; break;
                case "eqir": value = A == registers[B] ? 1 : 0; break;
                case "eqri": value = registers[A] == B ? 1 : 0; break;
                case "eqrr": value = registers[A] == registers[B] ? 1 : 0; break;
            }
            registers[C] = value;
            return registers;
        }

        static int Part1((int, Operation[]) data)
        {
            var (ip, operations) = data;
            var registers = new int[6];
            while (registers[ip] < operations.Count())
            {
                registers = RunOperation(registers, operations[registers[ip]]);
                registers[ip]++;
            }
            return registers[0];
        }

        static IEnumerable<int> GetDivisors(int number)
        {
            var largeDivisors = new List<int>();
            var top = (int)Math.Sqrt(number) + 1;
            for (var i = 1; i < top; i++)
                if (number % i == 0)
                {
                    yield return i;
                    if (i * i != number)
                        largeDivisors.Add(number / i);
                }
            largeDivisors.Reverse();
            foreach (var divisor in largeDivisors)
                yield return divisor;
        }

        static int Part2((int, Operation[]) data)
        {
            var (ip, operations) = data;
            var registers = new int[6];
            registers[0] = 1;
            while (registers[ip] != 1)
            {
                registers = RunOperation(registers, operations[registers[ip]]);
                registers[ip]++;
            }
            return GetDivisors(registers.First(register => register > 1 && register != 10550400)).Sum();
        }

        static (int, int) Solve((int, Operation[]) data)
            => (
                Part1(data),
                Part2(data)
            );

        static Regex operationRegex = new Regex(@"(?<opCode>\w+) (?<A>\d) (?<B>\d+) (?<C>\d+)", RegexOptions.Compiled);
        static (int, Operation[]) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var lines = File.ReadAllLines(filePath);
            return (int.Parse(lines[0].Split(" ")[1]), lines[1..].Select(line =>
            {
                var match = operationRegex.Match(line);
                if (match.Success)
                    return Tuple.Create(match.Groups["opCode"].Value, int.Parse(match.Groups["A"].Value), int.Parse(match.Groups["B"].Value), int.Parse(match.Groups["C"].Value));
                throw new Exception($"Bad format '{line}'");
            }).ToArray());
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
