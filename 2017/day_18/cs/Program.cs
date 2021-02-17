using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;

namespace AoC
{
    using Instructions = IEnumerable<(string mnemonic, string[] parameters)>;

    class Registers
    {
        public Registers() { }

        public long this[string key]
        {
            get
            {
                if (!_memory.ContainsKey(key))
                    _memory[key] = 0;
                return _memory[key];
            }
            set => _memory[key] = value;
        }

        private IDictionary<string, long> _memory = new Dictionary<string, long>();
    }

    class Computer
    {
        public int Id { get; init; }
        public bool Running { get; private set; } = true;
        public bool Outputting { get; private set; }
        public int OutputCount => _outputCount;
        public bool Polling { get; private set; }

        public Computer(Instructions instructions, int id, bool outputOnRcv = false)
        {
            _instructions = instructions.ToArray();
            Id = id;
            _outputOnRcv = outputOnRcv;
            _registers["p"] = id;
        }

        public bool IsActive() => Running && !Polling;
        public long GetOutput() => _outputs.Last();
        public void Connect(Computer other) => _outputs = other._inputs;

        public void Tick()
        {
            if (Running)
            {
                var instruction = _instructions.ElementAt((int)_pointer);
                _params = instruction.parameters;
                _pointer++;
                switch (instruction.mnemonic)
                {
                    case "set": _registers[_params[0]] = GetValue(1); break;
                    case "add": _registers[_params[0]] += GetValue(1); break;
                    case "mul": _registers[_params[0]] *= GetValue(1); break;
                    case "mod": _registers[_params[0]] %= GetValue(1); break;
                    case "snd":
                        _outputCount++;
                        _outputs.Enqueue(GetValue(0));
                        break;
                    case "rcv":
                        if (_outputOnRcv)
                            Outputting = true;
                        else if (_inputs.Any())
                        {
                            Polling = false;
                            _registers[_params[0]] = _inputs.Dequeue();
                        }
                        else
                        {
                            Polling = true;
                            _pointer--;
                        }
                        break;
                    case "jgz":
                        if (GetValue(0) > 0)
                            _pointer += GetValue(1) - 1;
                        break;
                }
            }
        }

        private long GetValue(int offset)
        {
            var value = _params[offset];
            if (long.TryParse(value, out var result))
                return result;
            return _registers[value];
        }

        private Instructions _instructions;
        private bool _outputOnRcv;
        private Registers _registers = new Registers();
        private long _pointer;
        private Queue<long> _outputs = new Queue<long>();
        private Queue<long> _inputs = new Queue<long>();
        private int _outputCount;
        private string[] _params;
    }

    static class Program
    {
        static long Part1(Instructions instructions)
        {
            var program = new Computer(instructions, 0, true);
            while (!program.Outputting)
                program.Tick();
            return program.GetOutput();
        }

        static int Part2(Instructions instructions)
        {
            var program0 = new Computer(instructions, 0);
            var program1 = new Computer(instructions, 1);
            program0.Connect(program1);
            program1.Connect(program0);
            while (program0.IsActive() || program1.IsActive())
            {
                program0.Tick();
                program1.Tick();
            }
            return program1.OutputCount;
        }

        static Instructions GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select(line =>
            {
                var splits = line.Split(' ');
                return (splits[0], splits[1..]);
            });
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
