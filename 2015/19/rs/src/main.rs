use regex::{Captures, Regex};
use std::collections::{HashMap, HashSet};

struct Replacement {
    source: String,
    target: String,
}

impl Replacement {
    fn regex(&self) -> Regex {
        Regex::new(&self.source).unwrap()
    }

    fn process(&self, molecule: &str) -> Vec<String> {
        let mut result = Vec::new();
        for cap in self.regex().captures_iter(molecule) {
            let mut new_molecule = String::default();
            new_molecule.push_str(&molecule[..cap.get(0).unwrap().start()]);
            new_molecule.push_str(&self.target);
            new_molecule.push_str(&molecule[cap.get(0).unwrap().end()..]);
            result.push(new_molecule);
        }
        result
    }
}

fn part1(puzzle_input: &(Vec<Replacement>, String)) -> usize {
    let (replacements, molecule) = puzzle_input;
    let mut new_molecules = HashSet::new();
    for replacement in replacements {
        for new_molecule in replacement.process(molecule) {
            new_molecules.insert(new_molecule);
        }
    }
    new_molecules.len()
}

fn part2(puzzle_input: &(Vec<Replacement>, String)) -> usize {
    let (replacements, molecule) = puzzle_input;
    let target_molecule = String::from("e");
    let mut molecule: String = molecule.chars().rev().collect();
    let replacement_dictionary: HashMap<String, String> = replacements
        .iter()
        .map(|rep| {
            (
                rep.target.chars().rev().collect(),
                rep.source.chars().rev().collect(),
            )
        })
        .collect();
    let expression: String = replacement_dictionary
        .keys()
        .map(|s| String::from(s))
        .collect::<Vec<String>>()
        .join("|");
    let replacements_regex = Regex::new(expression.as_str()).unwrap();
    let mut count = 0;
    while molecule != target_molecule {
        molecule = replacements_regex
            .replace(molecule.as_str(), |caps: &Captures| {
                replacement_dictionary
                    .get(caps.get(0).unwrap().as_str())
                    .unwrap()
            })
            .to_string();
        count += 1;
    }
    count
}

fn solve(puzzle_input: &(Vec<Replacement>, String)) -> (usize, usize) {
    (part1(puzzle_input), part2(puzzle_input))
}

fn get_input(file_path: &String) -> (Vec<Replacement>, String) {
    let line_regex = Regex::new(r"^(\w+)\s=>\s(\w+)$").unwrap();
    let mut replacements = Vec::new();
    let mut molecule = String::default();
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        if let Some(cap) = line_regex.captures(line) {
            replacements.push(Replacement {
                source: String::from(cap.get(1).unwrap().as_str()),
                target: String::from(cap.get(2).unwrap().as_str()),
            });
        } else {
            molecule.push_str(line);
        }
    }
    (replacements, String::from(molecule.trim()))
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
