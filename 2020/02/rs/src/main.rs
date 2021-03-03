use std::env;
use std::fs;
use std::time::{Instant};
use regex::Regex;

type Line = (usize, usize, char, String);

macro_rules! count_valid {
    ($lines: expr, $filter: expr) => {
        $lines.iter().filter($filter).count()
    };
}

fn solve(lines: &Vec<Line>) -> (usize,usize) {
    (
        count_valid!(lines, |line| {
            let (minimum, maximum, letter, password) = line;
            let occurence_count = password.chars().filter(|c| c == letter).count();
            occurence_count >= *minimum && occurence_count <= *maximum
        }),
        count_valid!(lines, |line| {
            let (first, second, letter, password) = line;
            (password.chars().nth(first - 1).unwrap() == *letter) 
            ^ 
            (password.chars().nth(second - 1).unwrap() == *letter)
        })
    )
}

fn get_input(file_path: &String) -> Vec<Line> {
    let re = Regex::new(r"^(\d+)-(\d+)\s([a-z]):\s(.*)$").unwrap();
    fs::read_to_string(file_path).expect("Error reading input file!")
        .lines()
        .map(|line| re.captures(line).and_then(|caps| 
            Some((
                caps.get(1)
                    .expect("Group not found in capture")
                    .as_str()
                    .parse()
                    .expect("Unable to parse number"),
                caps.get(2)
                    .expect("Group not found in capture")
                    .as_str()
                    .parse()
                    .expect("Unable to parse number"),
                caps.get(3)
                    .expect("Group not found in capture")
                    .as_str()
                    .chars()
                    .next()
                    .expect("Unable to retrieve first char of string"),
                String::from(caps.get(4)
                    .expect("Group not found in capture")
                    .as_str()
                )
            ))
        ).expect("Bad format"))
        .collect()
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
    println!("Time: {:.7}", now.elapsed().as_secs_f32());
}