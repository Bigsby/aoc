use std::env;
use std::fs;
use std::time::Instant;
use regex::Regex;
use std::collections::HashMap;

pub struct LogRecord {
    pub datetime: (u32, u32, u32, u32, u32),
    pub message: String,
}

pub struct GuardRecord {
    pub total: u32,
    pub minutes: Box<HashMap<u32, u32>>,
}

impl GuardRecord {
    fn new(total: u32) -> GuardRecord {
        GuardRecord {
            total,
            minutes: Box::new((0..60).map(|minute| (minute, 0u32)).collect()),
        }
    }
}

const FALL_ASLEEP: &str = "falls asleep";
const WAKE_UP: &str = "wakes up";
fn build_guard_records(log: Vec<LogRecord>) -> HashMap<u32, GuardRecord> {
    let shift_start_regex: Regex = Regex::new(r"^Guard\s#(?P<id>\d+)\sbegins\sshift").unwrap();
    let mut log = log;
    log.sort_by_key(|a| a.datetime);
    let mut guards: HashMap<u32, GuardRecord> = HashMap::new();
    let mut record_guard_times = |guard_id, last_asleep, woke| {
        if !guards.contains_key(&guard_id) {
            guards.insert(guard_id, GuardRecord::new(0));
        }
        let mut guard_record = guards.get_mut(&guard_id).unwrap();
        for minute in last_asleep..woke {
            *guard_record.minutes.get_mut(&minute).unwrap() += 1;
            guard_record.total += 1;
        }
    };
    let mut guard_id = 0;
    let mut guard_asleep = false;
    let mut last_asleep = 0;
    for log_record in log {
        let log_minutes = log_record.datetime.4;
        if log_record.message == FALL_ASLEEP {
            last_asleep = log_minutes;
            guard_asleep = true;
        } else if log_record.message == WAKE_UP {
            guard_asleep = false;
            record_guard_times(guard_id, last_asleep, log_minutes);
        } else if let Some(capture) = shift_start_regex.captures(&log_record.message) {
            if guard_asleep {
                record_guard_times(guard_id, last_asleep, 60);
                guard_asleep = false;
            }
            guard_id = capture.name("id").unwrap().as_str().parse().unwrap();
        }
    }
    guards
}

fn part1(guards: &HashMap<u32, GuardRecord>) -> u32 {
    let mut max_total = 0;
    let mut guard_id = 0;
    for (id, guard_record) in guards {
        if guard_record.total > max_total {
            max_total = guard_record.total;
            guard_id = *id;
        }
    }
    max_total = 0;
    let mut max_minute = Default::default();
    for (minute, total) in guards.get(&guard_id).unwrap().minutes.iter() {
        if *total > max_total {
            max_total = *total;
            max_minute = *minute;
        }
    }
    guard_id * max_minute
}

fn part2(guards: &HashMap<u32, GuardRecord>) -> u32 {
    let mut max_total = 0;
    let mut guard_id = 0;
    let mut max_minute = 0;
    for (id, guard_record) in guards {
        for (minute, total) in guard_record.minutes.iter() {
            if *total > max_total {
                max_total = *total;
                max_minute = *minute;
                guard_id = *id;
            }
        }
    }
    guard_id * max_minute
}

fn solve(guards: &HashMap<u32, GuardRecord>) -> (u32, u32) {
    (part1(guards), part2(guards))
}

fn parse_line(line: &str) -> LogRecord {
    let line_regex: Regex = Regex::new(r"\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2})\]\s(?P<message>.*)$").unwrap();
    line_regex
        .captures(line)
        .map(|cap| LogRecord {
            datetime: (
                cap.name("year").unwrap().as_str().parse().unwrap(),
                cap.name("month").unwrap().as_str().parse().unwrap(),
                cap.name("day").unwrap().as_str().parse().unwrap(),
                cap.name("hours").unwrap().as_str().parse().unwrap(),
                cap.name("minutes").unwrap().as_str().parse().unwrap(),
            ),
            message: String::from(cap.name("message").unwrap().as_str()),
        })
        .unwrap()
}

fn get_input(file_path: &String) -> HashMap<u32, GuardRecord> {
    build_guard_records(
        fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .lines()
            .map(|line| parse_line(line))
            .collect(),
    )
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}
