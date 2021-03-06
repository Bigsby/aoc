use regex::Regex;
use std::collections::{HashMap, HashSet};

type Record = (i32, Vec<String>);
type Records = HashMap<String, Record>;

fn part1(records: &Records) -> String {
    let mut all_children: HashSet<String> = HashSet::new();
    for (_, children) in records.values() {
        all_children = all_children
            .union(&children.iter().map(|child| String::from(child)).collect())
            .map(|child| String::from(child))
            .collect();
    }
    String::from(
        records
            .keys()
            .filter(|name| !all_children.contains(&String::from(*name)))
            .next()
            .expect("Top not found"),
    )
}

fn part2(records: &Records, top_tower: &str) -> i32 {
    let mut combined_weights = HashMap::new();
    while combined_weights.len() != records.len() {
        for (name, (weight, children)) in records {
            let mut weight_to_insert = 0;
            if combined_weights.contains_key(name) {
            } else if children.iter().count() == 0 {
                weight_to_insert = *weight;
            } else if children
                .iter()
                .all(|child| combined_weights.contains_key(child))
            {
                weight_to_insert = children.iter().fold(*weight, |acc, child| {
                    acc + *combined_weights.get(child).unwrap()
                });
            }
            if weight_to_insert != 0 {
                combined_weights.entry(name).or_insert(weight_to_insert);
            }
        }
    }
    let mut current_tower = records.get(&String::from(top_tower)).unwrap();
    let mut weight_difference = 0;
    loop {
        let (weight, children) = current_tower;
        let children_weights = children
            .iter()
            .map(|child| combined_weights.get(child).unwrap());
        let mut weight_counts = HashMap::new();
        for weight in children_weights {
            *weight_counts.entry(*weight).or_insert(0) += 1;
        }
        if weight_counts.len() == 1 {
            return weight + weight_difference;
        }
        let single_weight = weight_counts
            .iter()
            .filter(|(_, count)| **count == 1)
            .next()
            .unwrap()
            .0;
        weight_difference = weight_counts
            .iter()
            .filter(|(_, count)| **count > 1)
            .next()
            .unwrap()
            .0
            - single_weight;
        current_tower = records
            .get(
                children
                    .iter()
                    .filter(|child| combined_weights.get(child).unwrap() == single_weight)
                    .next()
                    .unwrap(),
            )
            .unwrap();
    }
}

fn solve(records: &Records) -> (String, i32) {
    let part1_result = part1(records);
    let another_tower = part1_result.clone();
    (part1_result, part2(records, another_tower.as_str()))
}

fn get_input(file_path: &String) -> Records {
    let line_regex =
        Regex::new(r"^(?P<name>[a-z]+)\s\((?P<weight>\d+)\)(?: -> )?(?P<children>.*)").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            if let Some(cap) = line_regex.captures(line) {
                return (
                    String::from(cap.name("name").unwrap().as_str()),
                    (
                        cap.name("weight").unwrap().as_str().parse().unwrap(),
                        cap.name("children")
                            .unwrap()
                            .as_str()
                            .trim()
                            .split(", ")
                            .filter(|child| !child.is_empty())
                            .map(|child| String::from(child))
                            .collect(),
                    ),
                );
            }
            panic!("Bad format '{}'", line)
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
    println!("Time: {:7}", end);
}
