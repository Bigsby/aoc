using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    static class Program
    {
        static (string token, string expression) GetNextToken(string expression)
        {
            var currentToken = string.Empty;
            foreach (var (c, index) in expression.Select((c, index) => (c, index)))
            {
                if (c == ' ')
                    return (currentToken, expression[Range.StartAt(index + 1)].Trim());
                if (currentToken.Any() && currentToken.All(char.IsDigit) && !char.IsDigit(c))
                    return (currentToken, expression[Range.StartAt(index)].Trim());
                currentToken += c;
            }
            return (currentToken, string.Empty);
        }

        static long PerformOperation(long first, string operation, long second)
        {
            switch(operation)
            {
                case "*": return first * second;
                case "+": return first + second;
                default: throw new Exception($"Unknow operation '{operation}'");
            }
        }

        static Regex parenRegex = new Regex(@"\((?<expression>[^()]+)\)", RegexOptions.Compiled);
        static Regex plusRegex = new Regex(@"(?<first>\d+)\s\+\s(?<second>\d+)", RegexOptions.Compiled);
        static long EvaluateExpression(string expression, bool addFirst)
        {
            var parenMatch = parenRegex.Match(expression);
            while (parenMatch.Success)
            {
                expression = 
                    expression[Range.EndAt(parenMatch.Index)] +
                    EvaluateExpression(parenMatch.Groups["expression"].Value, addFirst).ToString() +
                    expression[Range.StartAt(parenMatch.Index + parenMatch.Length)];
                parenMatch = parenRegex.Match(expression);
            }
            if (addFirst)
            {
                var plusMatch = plusRegex.Match(expression);
                while (plusMatch.Success)
                {
                    expression = 
                        expression[Range.EndAt(plusMatch.Index)] +
                        (long.Parse(plusMatch.Groups["first"].Value) + long.Parse(plusMatch.Groups["second"].Value)).ToString() +
                        expression[Range.StartAt(plusMatch.Index + plusMatch.Length)];
                    plusMatch = plusRegex.Match(expression);
                }
            }
            string token;
            (token, expression) = GetNextToken(expression);
            var currentValue = long.Parse(token);
            var operationToPeform = "";
            while (!string.IsNullOrEmpty(expression))
            {
                (token, expression) = GetNextToken(expression);
                if (long.TryParse(token, out var value))
                    currentValue = PerformOperation(currentValue, operationToPeform, value);
                else
                    operationToPeform = token;
            }
            return currentValue;
        }

        static long EvaluateExpressions(bool addFirst, IEnumerable<string> expressions)
            => expressions.Sum(expression => EvaluateExpression(expression, addFirst));

        static (long, long) Solve(IEnumerable<string> expressions)
            => (
                EvaluateExpressions(false, expressions),
                EvaluateExpressions(true, expressions)
            );

        static IEnumerable<string> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : File.ReadAllLines(filePath).Select(line => line.Trim());

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
