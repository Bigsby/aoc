use regex::Regex;
use std::collections::HashMap;

enum Rule {
    Letter(String),
    Set(Vec<Vec<u32>>),
}

impl Rule {
    fn parse(text: &str) -> Rule {
        if let Some(cap) = Regex::new("^\"(?P<letter>a|b)\"$").unwrap().captures(text) {
            Rule::Letter(String::from(cap.name("letter").unwrap().as_str()))
        } else {
            Rule::Set(
                text.split("|")
                    .map(|set| {
                        set.trim()
                            .split(" ")
                            .map(|rule| rule.trim().parse().unwrap())
                            .collect()
                    })
                    .collect(),
            )
        }
    }
}

fn generate_regex(
    rules: &HashMap<u32, Rule>,
    rule_number: u32,
    prefix: bool,
    sufix: bool,
) -> String {
    let rule = rules.get(&rule_number).unwrap();
    match rule {
        Rule::Letter(letter) => String::from(letter),
        Rule::Set(sets) => {
            let mut result = String::new();
            if prefix {
                result.push('^');
            }
            result.push_str("(?:");
            result.push_str(
                sets.iter()
                    .map(|rule_set| {
                        rule_set
                            .iter()
                            .map(|inner_number| generate_regex(rules, *inner_number, false, false))
                            .collect::<Vec<String>>()
                            .join("")
                    })
                    .collect::<Vec<String>>()
                    .join("|")
                    .as_str(),
            );
            result.push(')');
            if sufix {
                result.push('$');
            }
            result
        }
    }
}

fn is_inner_match(rule: &Regex, message: &str, position: usize) -> (bool, usize) {
    if let Some(cap) = rule.captures(&message[position..]) {
        (true, position + cap.get(0).unwrap().end())
    } else {
        (false, position)
    }
}

fn is_match(first_rule: &Regex, second_rule: &Regex, message: &str) -> bool {
    let mut count = 0;
    let (mut matched, mut position) = is_inner_match(first_rule, message, 0);
    while matched && position < message.len() {
        let last_position = position;
        for _ in 0..count {
            let (new_matched, new_position) = is_inner_match(second_rule, message, position);
            matched = new_matched;
            position = new_position;
            if !matched {
                position = last_position;
                break;
            } else if position == message.len() {
                return true;
            }
        }
        count += 1;
        let (new_matched, new_position) = is_inner_match(first_rule, message, position);
        matched = new_matched;
        position = new_position;
    }
    false
}

fn solve(puzzle_input: &(HashMap<u32, Rule>, Vec<String>)) -> (usize, usize) {
    let (rules, messages) = puzzle_input;
    let rule_0 = Regex::new(&generate_regex(rules, 0, true, true)).unwrap();
    let rule_42 = Regex::new(&generate_regex(rules, 42, true, false)).unwrap();
    let rule_31 = Regex::new(&generate_regex(rules, 31, true, false)).unwrap();
    (
        messages
            .iter()
            .filter(|message| rule_0.is_match(message))
            .count(),
        messages
            .iter()
            .filter(|message| is_match(&rule_42, &rule_31, message))
            .count(),
    )
}

fn get_input(file_path: &String) -> (HashMap<u32, Rule>, Vec<String>) {
    let rule_regex = Regex::new(r"(?P<number>^\d+):\s(?P<rule>.+)$").unwrap();
    let mut rules = HashMap::new();
    let mut messages = Vec::new();
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        if !line.is_empty() {
            if let Some(cap) = rule_regex.captures(line) {
                rules.insert(
                    cap.name("number").unwrap().as_str().parse().unwrap(),
                    Rule::parse(cap.name("rule").unwrap().as_str()),
                );
            } else {
                messages.push(String::from(line.trim()));
            }
        }
    }
    (rules, messages)
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
