using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    record Instruction;

    record MaskInstruction : Instruction
    {
        public string Mask { get; }
        public MaskInstruction(string mask)
            : base() => Mask = mask;
    }

    record MemoryInstruction : Instruction
    {
        public long Location { get; }
        public long Value { get; }
        public MemoryInstruction(long location, long value) : base()
        {
            Location = location;
            Value = value;
        }
    }

    class Computer
    {
        public long GetMemorySum() => _memory.Values.Sum();

        public void RunInstruction(Instruction instruction)
        {
            switch (instruction)
            {
                case MaskInstruction maskInstruction:
                    _mask = maskInstruction.Mask;
                    break;
                case MemoryInstruction memoryInstruction:
                    foreach (var location in GetMemoryLocations(memoryInstruction.Location))
                        _memory[location] = GetValue(memoryInstruction.Value);
                    break;
            }
        }

        protected virtual IEnumerable<long> GetMemoryLocations(long location)
        {
            yield return location;
        }
        protected virtual long GetValue(long value) => value;
        protected long GetOrMask() => Convert.ToInt64(_mask.Replace('X', '0'), 2);
        protected long GetAndMask() => Convert.ToInt64(_mask.Replace('X', '1'), 2);
        protected string _mask = new string('X', 36);
        Dictionary<long, long> _memory = new Dictionary<long, long>();
    }

    class ValueMaskComputer : Computer
    {
        protected override long GetValue(long value) => value | GetOrMask() & GetAndMask();
    }

    class MemoryMaskComputer : Computer
    {
        static void PrintList<T>(IEnumerable<T> list) => WriteLine("[ " + string.Join(",", list) + " ]");
        protected override IEnumerable<long> GetMemoryLocations(long location)
        {
            location |= GetOrMask();
            var maskBitOfffset = _mask.Length - 1;
            var flipBits = _xRegex.Matches(_mask).Select(match => maskBitOfffset - match.Index);
            foreach (var occurence in Enumerable.Range(0, 1 << flipBits.Count()))
            {
                var currentLocation = location;
                foreach (var (flipBit, index) in flipBits.Select((flipBit, index) => (flipBit, index)))
                {
                    currentLocation &= ~(1L << flipBit);
                    var newBit = ((1L << index) & occurence) >> index;
                    currentLocation |= newBit << flipBit;
                }
                yield return currentLocation;
            }
        }

        static Regex _xRegex = new Regex("X", RegexOptions.Compiled);
    }

    class Program
    {
        static long RunComputer(Computer computer, IEnumerable<Instruction> instructions)
        {
            foreach (var instruction in instructions)
                computer.RunInstruction(instruction);
            return computer.GetMemorySum();
        }

        static long Part1(IEnumerable<Instruction> instructions) => RunComputer(new ValueMaskComputer(), instructions);

        static long Part2(IEnumerable<Instruction> instructions) => RunComputer(new MemoryMaskComputer(), instructions);

        static Regex maskRegex = new Regex(@"^mask\s=\s(?<mask>[X01]+)$", RegexOptions.Compiled);
        static Regex memoryRegex = new Regex(@"^mem\[(?<location>[\d]+)]\s=\s(?<value>[\d]+)$", RegexOptions.Compiled);
        static IEnumerable<Instruction> GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return File.ReadLines(filePath).Select<string, Instruction>(line =>
            {
                var match = maskRegex.Match(line);
                if (match.Success)
                    return new MaskInstruction(match.Groups["mask"].Value);
                match = memoryRegex.Match(line);
                if (match.Success)
                    return new MemoryInstruction(long.Parse(match.Groups["location"].Value), long.Parse(match.Groups["value"].Value));
                throw new Exception($"Bad format '{line}'");
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