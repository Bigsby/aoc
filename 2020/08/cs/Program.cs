using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Instruction(string mnemonic, int argument);

    class Program
    {
        const string JMP = "jmp";
        const string NOP = "nop";
        const string ACC = "acc";

        static (int, int) RunInstruction(Instruction instruction, int accumulator, int instructionPointer)
            => (
                instruction.mnemonic == ACC ? accumulator + instruction.argument : accumulator,
                instructionPointer + (instruction.mnemonic == JMP ? instruction.argument : 1)
            );

        static (bool success, int accumulator) RunBoot(IEnumerable<Instruction> boot)
        {
            var bootArray = boot.ToArray();
            var accumulator = 0;
            var instructionPointer = 0;
            var visited = new List<int>();
            var bootLength = boot.Count();
            while (true)
            {
                visited.Add(instructionPointer);
                (accumulator, instructionPointer) = RunInstruction(bootArray[instructionPointer],
                                                        accumulator, instructionPointer);
                if (visited.Contains(instructionPointer))
                    return (false, accumulator);
                if (instructionPointer == bootLength)
                    return (true, accumulator);
            }
        }

        static (bool success, int accumulator) SwitchAndTest(int index, IEnumerable<Instruction> boot)
        {
            var bootArray = boot.ToArray();
            var (mnemonic, argument) = bootArray[index];
            bootArray[index] = new Instruction(mnemonic == JMP ? NOP : JMP, argument);
            return RunBoot(bootArray);
        }

        static int Part2(IEnumerable<Instruction> boot)
        {
            foreach (var index in Enumerable.Range(0, boot.Count()))
            {
                if (boot.ElementAt(index).mnemonic == ACC)
                    continue;
                var (success, accumulator) = SwitchAndTest(index, boot);
                if (success)
                    return accumulator;
            }
            throw new Exception("Valid boot not found");
        }

        static (int, int) Solve(IEnumerable<Instruction> boot)
            => (
                RunBoot(boot).accumulator,
                Part2(boot)
            );

        static Regex lineRegex = new Regex(@"^(nop|acc|jmp)\s\+?(-?\d+)$", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line =>
            {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return new Instruction(match.Groups[1].Value, int.Parse(match.Groups[2].Value));
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