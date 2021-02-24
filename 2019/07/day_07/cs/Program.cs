using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    class IntCodeComputer
    {   
        public bool Running { get; private set; } = true;

        public IntCodeComputer(int[] memory, IEnumerable<int> input)
        { 
            _memory = memory.ToArray();
            _input = new Queue<int>(input);
            _output = new Queue<int>();
        }

        public int Run()
        {
            while (Running) Tick();
            return _output.Dequeue();
        }

        public void AddInput(int value) => _input.Enqueue(value);

        public IEnumerable<int> GetOutputs() => _output.ToArray();

        public int GetOutput() => _output.Dequeue();

        public void Connect(IntCodeComputer other) => _output = other._input;

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
                    if (_input.Any())
                    {
                        _memory[GetAddress(1)] = _input.Dequeue();
                        _pointer += 2;
                    }
                    break;
                case 4: // OUTPUT
                    _output.Enqueue(GetParameter(1, p1Mode));
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
        private Queue<int> _input;
        private Queue<int> _output;
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
        static void PrintList<T>(IEnumerable<T> list)
        {
            WriteLine("[ " + string.Join(", ", list) + " ]");
        }

        static IEnumerable<IEnumerable<T>> Permutations<T>(IEnumerable<T> values) where T : IComparable<T>
        {
            if (values.Count() == 1)
                return new[] { values };
            return values.SelectMany(v => Permutations(values.Where(x => x.CompareTo(v) != 0)), (v, p) => p.Prepend(v));
        }

        static int RunPhasesPermutation(int[] memory, IEnumerable<int> phases)
        {
            var output = 0;
            foreach (var phase in phases)
                output = new IntCodeComputer(memory, new [] { phase, output }).Run();
            return output;
        }

        static int Part1(int[] memory)
            => Permutations(Enumerable.Range(0, 5)).Max(permutation => RunPhasesPermutation(memory, permutation));

        static int RunFeedbackPhasesPermutation(int[] memory, IEnumerable<int> phases)
        {
            var amplifiers = phases.Select(phase => new IntCodeComputer(memory, new [] { phase })).ToArray();
            amplifiers[0].AddInput(0);
            for (var i = 0; i < amplifiers.Length; i++)
                amplifiers[i].Connect(amplifiers[(i + 1) % amplifiers.Length]);
            while (amplifiers.Any(amplifier => amplifier.Running))
                foreach (var amplifier in amplifiers)
                    amplifier.Tick();
            return amplifiers[^1].GetOutput();
        }

        static int Part2(int[] memory)
            => Permutations(Enumerable.Range(5, 5)).Max(permutation => RunFeedbackPhasesPermutation(memory, permutation));

        static int[] GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadAllText(filePath).Trim().Split(",").Select(int.Parse).ToArray();
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