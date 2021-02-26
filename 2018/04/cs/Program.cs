using System;
using static System.Console;
using System.IO;
using System.Diagnostics;
using System.Linq;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace AoC
{
    struct LogRecord
    {
        public LogRecord(DateTime date, string message)
        {
            Date = date;
            Message = message;
        }
        public DateTime Date { get; }
        public string Message { get; }
    }

    struct GuardRecord
    {
        private GuardRecord(int total)
        {
            Total = 0;
            Minutes = new Dictionary<int, int>();
            foreach (var minute in Enumerable.Range(0, 60))
                Minutes[minute] = 0;
        }
        public int Total { get; set; }
        public Dictionary<int, int> Minutes { get; }

        public static GuardRecord New() => new GuardRecord(0);
    }

    class Program
    {
        static int Part1(Dictionary<int,GuardRecord> guards)
        {
            var guardId = guards.Aggregate((max, current) => max.Value.Total > current.Value.Total ? max : current).Key;
            var maxMinute = guards[guardId].Minutes.Aggregate((max, current) => max.Value > current.Value ? max : current).Key;
            return guardId * maxMinute;
        }

        static int Part2(Dictionary<int,GuardRecord> guards)
        {
            var maxTotal = 0;
            var maxMinute = -1;
            var guardId = -1;
            foreach (var (id, guardRecord) in guards.Select(pair => (pair.Key, pair.Value)))
                foreach (var (minute, total) in guardRecord.Minutes.Select(pair => (pair.Key, pair.Value)))
                    if (total > maxTotal)
                    {
                        maxTotal = total;
                        maxMinute = minute;
                        guardId = id;
                    }
            return guardId * maxMinute;
        }

        static GuardRecord RecordGuardTimes(int id, Dictionary<int, GuardRecord> guards, int lastAsleep, int woke)
        {
            if (!guards.ContainsKey(id))
                guards[id] = GuardRecord.New();
            var guardRecord = guards[id];
            foreach (var minute in Enumerable.Range(lastAsleep, woke - lastAsleep))
            {
                guardRecord.Total++;
                guardRecord.Minutes[minute]++;
            }
            return guardRecord;
        }

        static Regex shiftStartRegex = new Regex(@"^Guard\s#(?<id>\d+)\sbegins\sshift", RegexOptions.Compiled);
        const string FALL_ASLEEP = "falls asleep";
        const string WAKE_UP = "wakes up";
        static Dictionary<int,GuardRecord> BuildGuardRecords(IEnumerable<LogRecord> log)
        {
            var a = Tuple.Create(1, 2);
            log = log.OrderBy(record => record.Date);
            var guards = new Dictionary<int, GuardRecord>();
            var guardId = 0;
            var guardAsleep = false;
            var lastAsleep = 0;
            foreach (var record in log)
            {
                Match match = shiftStartRegex.Match(record.Message);
                if (match.Success) {
                    if (guardAsleep)
                    {
                        guards[guardId] = RecordGuardTimes(guardId, guards, lastAsleep, 60);
                        guardAsleep = false;
                    }
                    guardId = int.Parse(match.Groups["id"].Value);
                }
                else if (record.Message == FALL_ASLEEP)
                {
                    lastAsleep = record.Date.Minute;
                    guardAsleep = true;
                }
                else if (record.Message == WAKE_UP)
                {
                    guardAsleep = false;
                    guards[guardId] = RecordGuardTimes(guardId, guards, lastAsleep, record.Date.Minute);
                }
            }
            return guards;
        }

        static (int, int) Solve(Dictionary<int,GuardRecord> guards)
            => (
                Part1(guards),
                Part2(guards)
            );

        static Regex lineRegex = new Regex(@"\[(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2})\s(?<hours>\d{2}):(?<minutes>\d{2})\]\s(?<message>.*)$", RegexOptions.Compiled);
        static Dictionary<int,GuardRecord> GetInput(string filePath)
            => !File.Exists(filePath) ? throw new FileNotFoundException(filePath)
            : BuildGuardRecords(File.ReadLines(filePath).Select(line => {
                Match match = lineRegex.Match(line);
                if (match.Success)
                    return new LogRecord(
                        new DateTime(
                        int.Parse(match.Groups["year"].Value),
                        int.Parse(match.Groups["month"].Value),
                        int.Parse(match.Groups["day"].Value),
                        int.Parse(match.Groups["hours"].Value),
                        int.Parse(match.Groups["minutes"].Value), 0),
                        match.Groups["message"].Value
                    );
                throw new Exception($"Bad format '{line}");
            }));

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