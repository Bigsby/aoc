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

        public IntCodeComputer(int[] memory, int input)
        { 
            _memory = memory.ToArray();
            _input = input;
        }

        public int Run()
        {
            while (Running) Tick();
            return _output;
        }

        public void Tick()
        {            
            if (!Running) return;
            var instruction = _memory[_pointer];
            var (opCode, p1Mode, p2Mode) = (instruction % 100, (instruction / 100) % 10, (instruction / 1000) % 10);
            switch (opCode)
            {
                case 1: // ADD
                    _memory[GetAddress(3)] = GetParameter(1, p1Mode) + GetParameter(2, p2Mode);
                    _pointer += 4;
                    break;
                case 2: // MUL
                    _memory[GetAddress(3)] = GetParameter(1, p1Mode) * GetParameter(2, p2Mode);
                    _pointer += 4;
                    break;
                case 3: // INPUT
                    _memory[GetAddress(1)] = _input;
                    _pointer += 2;
                    break;
                case 4: // OUTPUT
                    _output = GetParameter(1, p1Mode);
                    _pointer += 2;
                    break;
                case 5: // JMP_TRUE
                    if (GetParameter(1, p1Mode) != 0)
                        _pointer = GetParameter(2, p2Mode);
                    else
                        _pointer += 3;
                    break;
                case 6: // JMP_FALSE
                    if (GetParameter(1, p1Mode) == 0)
                        _pointer = GetParameter(2, p2Mode);
                    else
                        _pointer += 3;
                    break;
                case 7: // LESS_THAN
                    _memory[GetAddress(3)] = GetParameter(1, p1Mode) < GetParameter(2, p2Mode) ? 1 : 0;
                    _pointer += 4;
                    break;
                case 8: // LESS_THAN
                    _memory[GetAddress(3)] = GetParameter(1, p1Mode) == GetParameter(2, p2Mode) ? 1 : 0;
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
        private int _input;
        private int _output;
        private int _pointer;
        private int GetAddress(int offset) => _memory[_pointer + offset];
        private int GetParameter(int offset, int mode) 
        {
            var value =  _memory[_pointer + offset];
            switch(mode)
            {
                case 0: // POSITION
                    return _memory[value];
                case 1: // IMMEDIATE
                    return value;
                default:
                    throw new Exception($"Unrecognized parameter mode '{mode}'");
            }
        } 
    }

    class Program
    {
        static (int, int) Solve(int[] memory)
            => (
                new IntCodeComputer(memory, 1).Run(),
                new IntCodeComputer(memory, 5).Run()
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