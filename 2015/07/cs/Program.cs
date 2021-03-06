using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Connections = Dictionary<string, Connection>;

    abstract record Operand
    {
        public static Operand Parse(string value)
        {
            if (int.TryParse(value, out var scalar))
                return new Scalar(scalar);
            return new Wire(value);
        }
    }

    record Scalar : Operand
    {
        public int Value { get; }
        public Scalar(int value) => Value = value;
    }

    record Wire : Operand
    {
        public string Source { get; }
        public Wire(string source) => Source = source;
    }

    enum Operation
    {
        And,
        Or,
        LShift,
        RShift,
    }

    abstract record Connection { }

    record Input : Connection
    {
        public Operand Operand { get; }
        public Input(Operand operand) => Operand = operand;
    }

    record Not : Connection
    {
        public Operand Operand { get; }
        public Not(Operand operand) => Operand = operand;
    }

    record Binary : Connection
    {
        public Operand Operand1 { get; }
        public Operand Operand2 { get; }
        public Operation Operation { get; }
        public Binary(Operand operand1, Operand operand2, Operation operation)
        {
            Operand1 = operand1;
            Operand2 = operand2;
            Operation = operation;
        }
    }

    class Circuit
    {
        public Circuit(Connections connections) => _connections = connections;

        public int SolverFor(string target, Dictionary<string, int> initialState)
        {
            _solutions = initialState;
            return GetValueFromConnection(target);
        }

        Connections _connections;
        Dictionary<string, int> _solutions = new Dictionary<string, int>();

        int GetValueFromOperand(Operand operand)
            => operand switch
            {
                Scalar scalar => scalar.Value,
                Wire wire => GetValueFromConnection(wire.Source),
                _ => throw new Exception($"Unknown operand type '{operand}'")
            };

        int GetValueFromBinaryConnection(Binary connection)
        {
            var x = GetValueFromOperand(connection.Operand1);
            var y = GetValueFromOperand(connection.Operand2);
            return connection.Operation switch
            {
                Operation.And => x & y,
                Operation.Or => x | y,
                Operation.LShift => x << y,
                Operation.RShift => x >> y,
                _ => throw new Exception($"Unknon binary operation '{connection.Operation}'")
            };
        }

        int CalculateValueForConnection(Connection connection)
            => connection switch
            {
                Input input => GetValueFromOperand(input.Operand),
                Not not => ~GetValueFromOperand(not.Operand),
                Binary binary => GetValueFromBinaryConnection(binary),
                _ => throw new Exception($"Unknown operation: '{connection}'")
            };

        int GetValueFromConnection(string target)
            => _solutions.ContainsKey(target)
            ? _solutions[target]
            : _solutions[target] = CalculateValueForConnection(_connections[target]);
    }

    class Program
    {
        static (int, int) Solve(Circuit circuit)
        {
            var startingTarget = "a";
            var part1 = circuit.SolverFor(startingTarget, new Dictionary<string, int>());
            var part2 = circuit.SolverFor(startingTarget, new Dictionary<string, int> { { "b", part1 } });
            return (part1, part2);
        }

        static Regex sourceTargetRegex = new Regex(@"^(.*)\s->\s(\w+)$", RegexOptions.Compiled);
        static Regex inputRegex = new Regex(@"^[^\s]+$", RegexOptions.Compiled);
        static Regex unaryRegex = new Regex(@"NOT\s(\w+)$", RegexOptions.Compiled);
        static Regex binaryRegex = new Regex(@"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)", RegexOptions.Compiled);
        static Circuit GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : new Circuit(File.ReadAllLines(filePath).Select<string, (string target, Connection connection)>(line =>
            {
                Match sourceTargetMatch = sourceTargetRegex.Match(line);
                if (sourceTargetMatch.Success)
                {
                    var (source, target) = (sourceTargetMatch.Groups[1].Value, sourceTargetMatch.Groups[2].Value);
                    if (inputRegex.Match(source).Success)
                        return (target, new Input(Operand.Parse(source)));
                    Match unaryMatch = unaryRegex.Match(source);
                    if (unaryMatch.Success)
                        return (target, new Not(Operand.Parse(unaryMatch.Groups[1].Value)));
                    Match binaryMatch = binaryRegex.Match(source);
                    if (binaryMatch.Success)
                        return (target, new Binary(
                            Operand.Parse(binaryMatch.Groups[1].Value), 
                            Operand.Parse(binaryMatch.Groups[3].Value), 
                            Enum.Parse<Operation>(binaryMatch.Groups[2].Value, true)));
                }
                throw new Exception($"Unrecognized connection: '{line}'");
            }).ToDictionary(pair => pair.target, pair => pair.connection));

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