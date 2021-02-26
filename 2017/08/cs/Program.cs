using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Instructions = IEnumerable<(string target, string source, Direction direction, int amount, Operator oper, int value)>;

    enum Direction
    {
        Increment,
        Decrement
    }

    enum Operator
    {
        Equal,
        NotEqual,
        LessThan,
        GreaterThan,
        LessOrEqual,
        GreatherOrEqual
    }
    
    class Program
    {
        static bool IsConditionValid(int source, Operator oper, int value)
        {
            switch(oper)
            {
                case Operator.Equal: return source == value;
                case Operator.NotEqual: return source != value;
                case Operator.LessThan: return source < value;
                case Operator.GreaterThan: return source > value;
                case Operator.LessOrEqual: return source <= value;
                case Operator.GreatherOrEqual: return source >= value;
                default: throw new Exception($"Unknow operator '{oper}'");
            }
        }

        static (int, int) Solve(Instructions instructions)
        {
            var memory = new Dictionary<string, int>();
            var maxValue = 0;
            foreach (var instruction in instructions)
            {
                var sourceValue = memory.ContainsKey(instruction.source) ? memory[instruction.source] : 0;
                if (!IsConditionValid(sourceValue, instruction.oper, instruction.value))
                    continue;
                if (!memory.ContainsKey(instruction.target))
                    memory[instruction.target] = 0;
                memory[instruction.target] += instruction.amount * (instruction.direction == Direction.Increment ? 1 : -1);
                maxValue = Math.Max(maxValue, memory[instruction.target]);
            }
            return (memory.Values.Max(), maxValue);
        }

        static Dictionary<string, Direction> DIRECTIONS = new Dictionary<string, Direction>
        {
            { "inc", Direction.Increment },
            { "dec", Direction.Decrement }
        };
        static Dictionary<string, Operator> OPEATORS = new Dictionary<string, Operator>
        {
            { "==", Operator.Equal },
            { "!=", Operator.NotEqual },
            { "<", Operator.LessThan },
            { ">", Operator.GreaterThan },
            { "<=", Operator.LessOrEqual },
            { ">=", Operator.GreatherOrEqual },
        };
        static Regex lineRegex = new Regex(@"^(?<target>[a-z]+)\s(?<direction>inc|dec)\s(?<amount>-?\d+)\sif\s(?<source>[a-z]+)\s(?<operator>==|!=|>=|<=|>|<)\s(?<value>-?\d+)$", RegexOptions.Compiled);
        static Instructions GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => {
                var match = lineRegex.Match(line);
                if (match.Success)
                    return (
                        match.Groups["target"].Value,
                        match.Groups["source"].Value,
                        DIRECTIONS[match.Groups["direction"].Value],
                        int.Parse(match.Groups["amount"].Value),
                        OPEATORS[match.Groups["operator"].Value],
                        int.Parse(match.Groups["value"].Value)
                    );
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