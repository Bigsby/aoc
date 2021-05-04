use regex::Regex;
use std::collections::HashMap;

enum Rule {
    Letter(char),
    Set(Vec<Vec<u32>>),
}

impl Rule {
    fn parse(text: &str) -> Self {
        if let Some(cap) = Regex::new("^\"(?P<letter>a|b)\"$").unwrap().captures(text) {
            Rule::Letter(cap.name("letter").unwrap().as_str().chars().next().unwrap())
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

    fn clone(&self) -> Self {
        match self {
            Rule::Letter(letter) => Rule::Letter(*letter),
            Rule::Set(sets) => Rule::Set(sets.clone()),
        }
    }
}

fn find_matched_indexes(
    rules: &HashMap<u32, Rule>,
    message: &str,
    rule_number: u32,
    index: usize,
) -> Vec<usize> {
    if index == message.len() {
        return vec![];
    }
    match rules.get(&rule_number).unwrap() {
        Rule::Letter(letter) => {
            if message.chars().nth(index).unwrap() == *letter {
                vec![index + 1]
            } else {
                vec![]
            }
        }
        Rule::Set(sets) => {
            let mut matches = Vec::new();
            for rule_set in sets {
                let mut sub_matches = vec![index];
                for sub_rule in rule_set {
                    let mut new_matches = Vec::new();
                    for sub_match_index in sub_matches.iter() {
                        new_matches.append(&mut find_matched_indexes(
                            rules,
                            message,
                            *sub_rule,
                            *sub_match_index,
                        ));
                    }
                    sub_matches = new_matches;
                }
                matches.append(&mut sub_matches);
            }
            matches
        }
    }
}

fn solve(puzzle_input: &(HashMap<u32, Rule>, Vec<String>)) -> (usize, usize) {
    let (rules, messages) = puzzle_input;
    let part1_result = messages
        .iter()
        .filter(|message| find_matched_indexes(rules, message, 0, 0).contains(&message.len()))
        .count();
    let mut rules: HashMap<u32, Rule> = rules
        .into_iter()
        .map(|(rule_number, rule)| (*rule_number, rule.clone()))
        .collect();
    *rules.get_mut(&8).unwrap() = Rule::parse("42 | 42 8");
    *rules.get_mut(&11).unwrap() = Rule::parse("42 31 | 42 11 31");
    (
        part1_result,
        messages
            .iter()
            .filter(|message| find_matched_indexes(&rules, message, 0, 0).contains(&message.len()))
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
