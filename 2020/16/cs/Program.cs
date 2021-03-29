using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    using Ticket = List<int>;
    using Rule = Tuple<string, int, int, int, int>;

    static class Program
    {
        static IEnumerable<int> GetValidNumbers(IEnumerable<Rule> rules)
        {
            var validNumbers = new HashSet<int>();
            foreach (var (_, startOne, endOne, startTwo, endTwo) in rules)
            {
                foreach (var number in Enumerable.Range(startOne, endOne - startOne + 1))
                    validNumbers.Add(number);
                foreach (var number in Enumerable.Range(startTwo, endTwo - startTwo + 1))
                    validNumbers.Add(number);
            }
            return validNumbers;
        }

        static int Part1(IEnumerable<Ticket> tickets, IEnumerable<int> validNumbers)
        {
            var total = 0;
            foreach (var ticket in tickets)
                foreach (var number in ticket)
                    if (!validNumbers.Contains(number))
                        total += number;
            return total;
        }

        static long Part2(IEnumerable<Rule> rules, Ticket myTicket, IEnumerable<Ticket> tickets, IEnumerable<int> validNumbers)
        {
            var validTickets = tickets.Where(ticket => ticket.All(number => validNumbers.Contains(number)));
            var ranges = rules.ToDictionary(rule => rule.Item1, rule => (rule.Item2, rule.Item3, rule.Item4, rule.Item5));
            var positions = rules.ToDictionary(rule => rule.Item1, _ => Enumerable.Range(0, rules.Count()).ToList());
            var names = rules.Select(rule => rule.Item1);
            foreach (var ticket in validTickets)
                foreach (var (number, index) in ticket.Select((number, index) => (number, index)))
                    foreach (var fieldName in names)
                    {
                        if (!positions[fieldName].Contains(index))
                            continue;
                        var (startOne, endOne, startTwo, endTwo) = ranges[fieldName];
                        if (number < startOne || (number > endOne && number < startTwo) || number > endTwo)
                        {
                            var toRemove = new Stack<(string ownerName, int positionToRemove)>();
                            positions[fieldName].Remove(index);
                            if (positions[fieldName].Count == 1)
                                toRemove.Push((fieldName, positions[fieldName].First()));
                            while (toRemove.Any())
                            {
                                var (ownerName, positionToRemove) = toRemove.Pop();
                                foreach (var otherFieldName in names)
                                {
                                    if (otherFieldName == ownerName || !positions[otherFieldName].Contains(positionToRemove))
                                        continue;
                                    positions[otherFieldName].Remove(positionToRemove);
                                    if (positions[otherFieldName].Count == 1)
                                        toRemove.Push((otherFieldName, positions[otherFieldName].First()));
                                }
                            }
                        }
                    }
            var departureFieldIndexes = names.Where(name => name.StartsWith("departure")).Select(name => positions[name].First());
            return departureFieldIndexes.Aggregate(1L, (soFar, index) => soFar * myTicket.ElementAt(index));
        }

        static (int, long) Solve((IEnumerable<Rule> rules, Ticket myTicket, IEnumerable<Ticket> tickets) puzzleInput)
        {
            var (rules, myTicket, tickets) = puzzleInput;
            var validNumbers = GetValidNumbers(rules);
            return (
                Part1(tickets, validNumbers),
                Part2(rules, myTicket, tickets, validNumbers)
            );
        }

        static Regex fieldRegex = new Regex(@"^(?<field>[^:]+):\s(?<r1s>\d+)-(?<r1e>\d+)\sor\s(?<r2s>\d+)-(?<r2e>\d+)$", RegexOptions.Compiled);
        static Regex ticketRegex = new Regex(@"^(?:\d+\,)+(?:\d+$)", RegexOptions.Compiled);
        static (IEnumerable<Rule> rules, Ticket myTicket, IEnumerable<Ticket> tickets) GetInput(string filePath)
        {
            if (!File.Exists(filePath)) throw new FileNotFoundException(filePath);
            var rules = new List<Rule>();
            var myTicket = new Ticket();
            var tickets = new List<Ticket>();
            var doingRules = true;
            var doingMyTicket = true;
            foreach (var line in File.ReadAllLines(filePath))
            {
                if (doingRules)
                {
                    var fieldMatch = fieldRegex.Match(line);
                    if (fieldMatch.Success)
                        rules.Add(Tuple.Create(
                            fieldMatch.Groups["field"].Value,
                            int.Parse(fieldMatch.Groups["r1s"].Value),
                            int.Parse(fieldMatch.Groups["r1e"].Value),
                            int.Parse(fieldMatch.Groups["r2s"].Value),
                            int.Parse(fieldMatch.Groups["r2e"].Value)
                        ));
                    else
                        doingRules = false;
                }
                var ticketMatch = ticketRegex.Match(line);
                if (!ticketMatch.Success)
                    continue;
                if (doingMyTicket)
                {
                    myTicket = line.Split(',').Select(int.Parse).ToList();
                    doingMyTicket = false;
                }
                else
                    tickets.Add(line.Split(',').Select(int.Parse).ToList());
            }
            return (rules, myTicket, tickets);
        }

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
