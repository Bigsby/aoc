using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Instruction = List<string>;

    static class Program
    {
        static Dictionary<string, string> INSTRUCTION_TOGGLE = new Dictionary<string, string> {
            { "inc", "dec" },
            { "dec", "inc" },
            { "tgl", "inc" },
            { "jnz", "cpy" },
            { "cpy", "jnz" }
        };
        static int RunInstructions(Instruction[] instructions, Dictionary<string, int> inputs)
        {
            instructions = instructions.ToArray();
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
                        {
                            var jumpOffset = 0;
                            if (!int.TryParse(jumpValue, out jumpOffset))
                                jumpOffset = registers[jumpValue];
                            pointer += jumpOffset;
                        }
                        else
                            pointer++;
                        break;
                    case "tgl":
                        var offset = 0;
                        if (!int.TryParse(instruction[1], out offset))
                            offset = registers[instruction[1]];
                        var pointerToChange = pointer + offset;
                        if (pointerToChange >= 0 && pointerToChange < instructions.Length)
                        {
                            var currentInstruction = instructions[pointerToChange];
                            instructions[pointerToChange] = new [] { INSTRUCTION_TOGGLE[currentInstruction[0]]}.Concat(currentInstruction.Skip(1)).ToList();
                        }
                        pointer++;
                        break;
                }
            }
            return registers["a"];
        }

        static (int, int) Solve(Instruction[] instructions)
        {
            var a = int.Parse(instructions[19][1]);
            var b = int.Parse(instructions[20][1]);
            return (
                RunInstructions(instructions, new Dictionary<string, int> { { "a", 7 } }),
                Enumerable.Range(1, 12).Aggregate((soFar, current) => soFar * current) + a * b
            );
        }

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
