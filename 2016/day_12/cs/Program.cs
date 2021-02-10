using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Instruction = List<string>;

    class Program
    {
        static int RunInstructions(Instruction[] instructions, Dictionary<string, int> inputs)
        {
            var registers = new[] { "a", "b", "c", "d" }.ToDictionary(value => value, value => 0);
            foreach (var register in inputs.Keys)
                registers[register] = inputs[register];
            var pointer = 0;
            while (pointer < instructions.Length)
            {
                var instruction = instructions[pointer];
                var mnemonic = instruction[0];
                switch (mnemonic)
                {
                    case "cpy":
                        var (sourceParam, targetParam) = (instruction[1], instruction[2]);
                        var value = 0;
                        if (!int.TryParse(sourceParam, out value))
                            value = registers[sourceParam];
                        registers[targetParam] = value;
                        pointer++;
                        break;
                    case "inc":
                        registers[instruction[1]]++;
                        pointer++;
                        break;
                    case "dec":
                        registers[instruction[1]]--;
                        pointer++;
                        break;
                    case "jnz":
                        var (condition, jumpValue) = (instruction[1], instruction[2]);
                        var conditionValue = 0;
                        if (!int.TryParse(condition, out conditionValue))
                            conditionValue = registers[condition];
                        if (conditionValue != 0)
                            pointer += int.Parse(jumpValue);
                        else
                            pointer++;
                        break;
                }
            }
            return registers["a"];
        }

        static int Part1(Instruction[] instructions)
            =>  RunInstructions(instructions, new Dictionary<string, int>());

        static int Part2(Instruction[] instructions)
            =>  RunInstructions(instructions, new Dictionary<string, int> { { "c", 1 } });

        static Instruction[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllLines(filePath).Select(line => {
                var mnemonic = line[..3];
                var parameters = line[3..].Trim().Split(" ").ToList();
                parameters.Insert(0, mnemonic);
                return parameters;
            }).ToArray();
        }

        static void Main(string[] args)
        {
            if (args.Length != 1) throw new Exception("Please, add input file path as parameter");

            var puzzleInput = GetInput(args[0]);
            var watch = Stopwatch.StartNew();
            var part1Result = Part1(puzzleInput);
            watch.Stop();
            var middle = watch.ElapsedTicks;
            watch = Stopwatch.StartNew();
            var part2Result = Part2(puzzleInput);
            watch.Stop();
            WriteLine($"P1: {part1Result}");
            WriteLine($"P2: {part2Result}");
            WriteLine();
            WriteLine($"P1 time: {(double)middle / 100 / TimeSpan.TicksPerSecond:f7}");
            WriteLine($"P2 time: {(double)watch.ElapsedTicks / 100 / TimeSpan.TicksPerSecond:f7}");
        }
    }
}