using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    class Program
    {
        const string WIRE = "wire", SCALAR = "scalar";
        const string INPUT = "input", UNARY = "unary", BINARY = "binary";
 
        record Operand
        {
            public Operand(string value)
            {
                try
                {
                    Scalar = int.Parse(value);
                    Type = SCALAR;
                }
                catch
                {
                    Wire = value;
                }
            }
            public string Type { get; } = WIRE;
            public int Scalar { get; } = 0;
            public string Wire { get; } = string.Empty;
        }

        record Connection
        {
            public Connection(string operation, string type, string operand1, string operand2, string target)
            {
                Operation = operation;
                Type = type;
                Operand1 = new Operand(operand1);
                if (!string.IsNullOrEmpty(operand2))
                    Operand2 = new Operand(operand2);
                Target = target;
            }
            public string Operation { get; }
            public string Type { get; }
            public Operand Operand1 { get; }
            public Operand Operand2 { get; }
            public string Target { get; }
        }

        static Dictionary<string, Func<int, int, int>> BINARY_OPERATIONS = new Dictionary<string, Func<int, int, int>>
        {
            { "AND", (x, y) => x & y },
            { "OR", (x, y) => x | y },
            { "LSHIFT", (x, y) => x << y },
            { "RSHIFT", (x, y) => x >> y },
        };
        
        class Circuit
        {
            public Circuit(IEnumerable<Connection> connections) => _connections = connections;

            public int SolverFor(string target, Dictionary<string, int> initialState)
            {
                _solutions = initialState;
                return GetValueFromConnection(GetConnectionFromTarget(target));
            }

            IEnumerable<Connection> _connections;
            Dictionary<string, int> _solutions = new Dictionary<string, int>();

            Connection GetConnectionFromTarget(string target)
                => _connections.First(connection => connection.Target == target);
            
            int GetValueFromOperand(Operand operand)
                => operand.Type == SCALAR ? operand.Scalar : GetValueFromConnection(GetConnectionFromTarget(operand.Wire));

            int GetValueFromBinaryConnection(Connection connection)
                => BINARY_OPERATIONS[connection.Operation](GetValueFromOperand(connection.Operand1), GetValueFromOperand(connection.Operand2));

            int CalculateValueForConnection(Connection connection)
            {
                switch (connection.Type)
                {
                    case INPUT:
                        return GetValueFromOperand(connection.Operand1);
                    case UNARY:
                        return ~GetValueFromOperand(connection.Operand1);
                    case BINARY:
                        return GetValueFromBinaryConnection(connection);
                    default:
                        throw new Exception($"Unknown operation: '{connection.Type}'");
                }
            }

            int GetValueFromConnection(Connection connection)
                => _solutions.ContainsKey(connection.Target) 
                ? _solutions[connection.Target] 
                : _solutions[connection.Target] = CalculateValueForConnection(connection);            
        }

        const int MAX_VALUE = 1 << 17;
        static int RunCode(Circuit circuit, bool reRunB)
        {
            var startingTarget = "a";
            var result = circuit.SolverFor(startingTarget, new Dictionary<string, int>());
            if (reRunB)
                result = circuit.SolverFor(startingTarget, new Dictionary<string, int> { { "b", result } });
            if (result < 0)
                result += MAX_VALUE;
            return result;
        }

        static int Part1(Circuit circuit) => RunCode(circuit, false);

        static int Part2(Circuit circuit) => RunCode(circuit, true);

        static Regex sourceTargetRegex = new Regex(@"^(.*)\s->\s(\w+)$", RegexOptions.Compiled);
        static Regex inputRegex = new Regex(@"^[^\s]+$", RegexOptions.Compiled);
        static Regex unaryRegex = new Regex(@"NOT\s(\w+)$", RegexOptions.Compiled);
        static Regex binaryRegex = new Regex(@"^(\w+|\d+)\s+(AND|OR|LSHIFT|RSHIFT)\s+(\w+|\d+)", RegexOptions.Compiled);
        static Circuit GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            return new Circuit(File.ReadAllLines(filePath).Select(line => {
                Match sourceTargetMatch = sourceTargetRegex.Match(line);
                if (sourceTargetMatch.Success)
                {
                    var (source, target) = (sourceTargetMatch.Groups[1].Value, sourceTargetMatch.Groups[2].Value);
                    if (inputRegex.Match(source).Success)
                        return new Connection(null, INPUT, source, null, target);
                    Match unaryMatch = unaryRegex.Match(source);
                    if (unaryMatch.Success)
                        return new Connection(null, UNARY, unaryMatch.Groups[1].Value, null, target);
                    Match binaryMatch = binaryRegex.Match(source);
                    if (binaryMatch.Success)
                        return new Connection(binaryMatch.Groups[2].Value, BINARY, binaryMatch.Groups[1].Value, binaryMatch.Groups[3].Value, target);
                }
                throw new Exception($"Unrecognized connection: '{line}'");
            }));
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