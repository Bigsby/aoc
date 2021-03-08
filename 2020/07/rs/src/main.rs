use regex::Regex;
use std::collections::HashSet;
use std::collections::{HashMap, VecDeque};

type Rule = (String, u32);
type Rules = HashMap<String, Vec<Rule>>;
const REQUIRED_COLOR: &str = "shiny gold";

fn get_rules_containing(color: String, rules: &Rules) -> usize {
    let mut result = HashSet::new();
    let mut to_process = VecDeque::new();
    to_process.push_back(color);
    while !to_process.is_empty() {
        let color = to_process.pop_front().unwrap();
        for (rule_color, inner_rules) in rules {
            if inner_rules.iter().any(|inner_rule| inner_rule.0 == color) {
                result.insert(String::from(rule_color));
                to_process.push_back(String::from(rule_color));
            }
        }
    }
    result.len()
}

fn get_quantity_from_color(color: String, rules: &Rules) -> u32 {
    rules
        .get(&color)
        .unwrap()
        .iter()
        .map(|(inner_color, quantity)| {
            quantity * (1 + get_quantity_from_color(String::from(inner_color), rules))
        })
        .sum()
}

fn solve(rules: &Rules) -> (usize, u32) {
    (
        get_rules_containing(String::from(REQUIRED_COLOR), rules),
        get_quantity_from_color(String::from(REQUIRED_COLOR), rules),
    )
}

fn process_inner_rules(text: String) -> Vec<Rule> {
    let inner_bags_regex = Regex::new(r"^(\d+)\s(.*)\sbags?$").unwrap();
    let text = text.strip_suffix(".").unwrap();
    if text == "no other bags" {
        vec![]
    } else {
        text.split(", ")
            .map(|inner_rule_text| {
                inner_bags_regex
                    .captures(inner_rule_text)
                    .map(|cap| {
                        (
                            String::from(cap.get(2).unwrap().as_str()),
                            cap.get(1).unwrap().as_str().parse().unwrap(),
                        )
                    })
                    .unwrap()
            })
            .collect()
    }
}

fn get_input(file_path: &String) -> Rules {
    let bags_regex = Regex::new(r"^(.*)\sbags contain\s(.*)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            bags_regex
                .captures(line)
                .map(|cap| {
                    (
                        String::from(cap.get(1).unwrap().as_str()),
                        process_inner_rules(String::from(cap.get(2).unwrap().as_str())),
                    )
                })
                .unwrap()
        })
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
