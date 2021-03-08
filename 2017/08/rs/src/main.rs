use std::collections::HashMap;
use regex::Regex;

type Instruction = (String, String, Direction, i32, Operator, i32);

enum Direction {
    Inc,
    Dec,
}

impl Direction {
    fn parse(value: &str) -> Direction {
        match value {
            "inc" => Direction::Inc,
            "dec" => Direction::Dec,
            _ => panic!("Unknown direction '{}'", value),
        }
    }
}

enum Operator {
    Equal,
    NotEqual,
    LessThan,
    GreaterThan,
    LessOrEqual,
    GreatherOrEqual,
}

impl Operator {
    fn parse(value: &str) -> Operator {
        match value {
            "==" => Operator::Equal,
            "!=" => Operator::NotEqual,
            "<" => Operator::LessThan,
            ">" => Operator::GreaterThan,
            "<=" => Operator::LessOrEqual,
            ">=" => Operator::GreatherOrEqual,
            _ => panic!("Uknown operator '{}'", value),
        }
    }
}

fn is_condition_valid(source: i32, operator: &Operator, value: i32) -> bool {
    match operator {
        Operator::Equal => source == value,
        Operator::NotEqual => source != value,
        Operator::LessThan => source < value,
        Operator::GreaterThan => source > value,
        Operator::LessOrEqual => source <= value,
        Operator::GreatherOrEqual => source >= value,
    }
}

fn solve(instructions: &Vec<Instruction>) -> (i32, i32) {
    let mut memory = HashMap::new();
    let mut max_value = 0;
    for (target, source, direction, amount, operator, value) in instructions {
        let source_value = *memory.entry(source).or_insert(0);
        if !is_condition_valid(source_value, operator, *value) {
            continue;
        }
        *memory.entry(target).or_insert(0) += amount * match direction {
            Direction::Inc => 1,
            Direction::Dec => -1,
        };
        max_value = max_value.max(*memory.get(target).unwrap());
    };
    (*memory.values().max().unwrap(), max_value)
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    let re = Regex::new(r"^(?P<target>[a-z]+)\s(?P<direction>inc|dec)\s(?P<amount>-?\d+)\sif\s(?P<source>[a-z]+)\s(?P<operator>==|!=|>=|<=|>|<)\s(?P<value>-?\d+)$").unwrap();
    std::fs::read_to_string(file_path).expect("Error reading input file!")
    .lines()
    .map(|line| re.captures(line).map(|cap| (
        String::from(cap.name("target").unwrap().as_str()),
        String::from(cap.name("source").unwrap().as_str()),
        Direction::parse(cap.name("direction").unwrap().as_str()),
        cap.name("amount").unwrap().as_str().parse().unwrap(),
        Operator::parse(cap.name("operator").unwrap().as_str()),
        cap.name("value").unwrap().as_str().parse().unwrap()
    )).unwrap())
    .collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = std::time::Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    let end = now.elapsed().as_secs_f32();
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
