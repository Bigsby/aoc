using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Instruction = Tuple<int, string ,int>;

    static class Program
    {
        const int HLF = 0; 
        const int TPL = 1; 
        const int INC = 2; 
        const int JMP =3; 
        const int JIE = 4; 
        const int JIO = 5;

        static int RunProgram(Instruction[] instructions, Dictionary<string, int> init = null)
        {
            var registers = new [] { "a", "b" }.ToDictionary(key => key, _ => 0);
            if (init is not null)
                foreach (var pair in init)
                    registers[pair.Key] = pair.Value;
            var pointer = 0;
            while (pointer < instructions.Length)
            {
                var (mnemonic, register, value) = instructions[pointer];
                var jump = 1;
                switch (mnemonic)
                {
                    case HLF: registers[register] /= 2; break;
                    case TPL: registers[register] *= 3; break;
                    case INC: registers[register]++; break;
                    case JMP: jump = value; break;
                    case JIE: if (registers[register] % 2 == 0) jump = value; break;
                    case JIO: if (registers[register] == 1) jump = value; break;
                }
                pointer += jump;
            }
            return registers["b"];
        }

        static int Part1(Instruction[] instructions)
            => RunProgram(instructions);

        static int Part2(Instruction[] instructions)
            => RunProgram(instructions, new Dictionary<string, int> { { "a", 1 } });

        static Dictionary<string, Func<string, Instruction>> INSTRUCTION_PARSERS = new Dictionary<string, Func<string, Instruction>>{
            { "hlf", line => Tuple.Create(HLF, line.Split(" ")[1], 0) },
            { "tpl", line => Tuple.Create(TPL, line.Split(" ")[1], 0) },
            { "inc", line => Tuple.Create(INC, line.Split(" ")[1], 0) },
            { "jmp", line => Tuple.Create(JMP, "", int.Parse(line.Split(" ")[1])) },
            { "jie", line => Tuple.Create(JIE, line.Split(" ")[1][..^1], int.Parse(line.Split(" ")[2])) },
            { "jio", line => Tuple.Create(JIO, line.Split(" ")[1][..^1], int.Parse(line.Split(" ")[2])) },
        };
        static Instruction[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line => {
                foreach (var key in INSTRUCTION_PARSERS.Keys)
                    if (line.StartsWith(key))
                        return INSTRUCTION_PARSERS[key](line);
                throw new Exception($"Bad format '{line}'");
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
