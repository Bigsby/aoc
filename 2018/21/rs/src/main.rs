use regex::Regex;
use std::collections::HashSet;

type Operation = (String, i64, i64, i64);

const MASK: i64 = 16777215;
const MULTIPLIER: i64 = 65899;

fn solve(data: &(usize, Vec<Operation>)) -> (i64, i64) {
    let (_, operations) = data;
    let magic_number = operations[7].1;
    let mut part1_result = 0;
    let mut seen = HashSet::new();
    let mut result = 0;
    let mut last_result = -1;
    loop {
        let mut accumulator = result | 0x10000;
        result = magic_number;
        loop {
            result = (((result + (accumulator & 0xFF)) & MASK) * MULTIPLIER) & MASK;
            if accumulator <= 0xFF {
                if part1_result == 0 {
                    part1_result = result;
                } else {
                    if seen.insert(result) {
                        last_result = result;
                        break;
                    } else {
                        return (part1_result, last_result);
                    }
                }
            } else {
                accumulator /= 0x100;
            }
        }
    }
}

fn get_input(file_path: &String) -> (usize, Vec<Operation>) {
    let operation_regex =
        Regex::new(r"^(?P<mnemonic>\w+) (?P<A>\d+) (?P<B>\d+) (?P<C>\d+)$").unwrap();
    let lines: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|s| String::from(s))
        .collect();
    (
        lines[0].split(" ").collect::<Vec<&str>>()[1]
            .parse()
            .unwrap(),
        lines
            .iter()
            .skip(1)
            .map(|line| {
                operation_regex
                    .captures(line)
                    .map(|cap| {
                        (
                            String::from(cap.name("mnemonic").unwrap().as_str()),
                            cap.name("A").unwrap().as_str().parse().unwrap(),
                            cap.name("B").unwrap().as_str().parse().unwrap(),
                            cap.name("C").unwrap().as_str().parse().unwrap(),
                        )
                    })
                    .unwrap()
            })
            .collect(),
    )
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
