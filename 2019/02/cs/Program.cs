using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;

namespace AoC
{
    class IntCodeComputer
    {   
        public bool Running { get; private set; } = true;

        public IntCodeComputer(int[] memory) => _memory = memory.ToArray();

        public int Run()
        {
            while (Running) Tick();
            return _memory[0];
        }

        public void Tick()
        {            
            if (!Running) return;
            var opCode = _memory[_pointer];
            switch (opCode)
            {
                case 1: // ADD
                    _memory[GetAddress(3)] = GetParameter(1) + GetParameter(2);
                    _pointer += 4;
                    break;
                case 2: // MUL
                    _memory[GetAddress(3)] = GetParameter(1) * GetParameter(2);
                    _pointer += 4;
                    break;
                case 99: // HATL
                    Running = false;
                    break;
                default:
                    throw new Exception($"Unknown instruction {_pointer} {opCode}");
            }
        }

        private int[] _memory;
        private int _pointer;
        private int GetAddress(int offset) => _memory[_pointer + offset];
        private int GetParameter(int offset) => _memory[_memory[_pointer + offset]];
    }

    class Program
    {
        static int RunProgram(int[] memory, int noun, int verb)
        {
            memory[1] = noun;
            memory[2] = verb;
            return new IntCodeComputer(memory).Run();
        }

        static int TARGET_VALUE = 19690720;
        static int Part2(int[] memory)
        {
            var range = Enumerable.Range(0, 100);
            foreach (var noun in range)
                foreach (var verb in range)
                    if (RunProgram(memory, noun, verb) == TARGET_VALUE)
                        return 100 * noun + verb;
            throw new Exception("Target value not found");
        }

        static (int, int) Solve(int[] memory)
            => (
                RunProgram(memory, 12, 2),
                Part2(memory)
            );

        static int[] GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllText(filePath).Trim().Split(",").Select(int.Parse).ToArray();

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