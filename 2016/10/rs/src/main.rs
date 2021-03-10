use regex::Regex;
use std::collections::HashMap;

type ValueInstruction = (u32, u32);
type CompareInstruction = (String, u32, String, u32);

fn solve(instructions: &(Vec<ValueInstruction>, HashMap<u32, CompareInstruction>)) -> (u32, u32) {
    const LOW_VALUE: u32 = 17;
    const HIGH_VALUE: u32 = 61;
    let target_outputs = vec![0, 1, 2];
    let (value_instructions, compare_instructions) = instructions;
    let mut bots: HashMap<u32, Vec<u32>> = HashMap::new();
    for (bot, value) in value_instructions {
        bots.entry(*bot).or_insert(Vec::new()).push(*value);
    }
    let mut outputs = HashMap::new();
    let mut part1_result = 0;
    let mut part2_result = 0;
    while part1_result == 0 || part2_result == 0 {       
        let (bot, chips) = bots
            .iter()
            .filter(|(_, chips)| chips.len() == 2)
            .next()
            .unwrap();
        let chips = chips.clone();
        let bot = *bot;
        let low_chip = *chips.iter().min().unwrap();
        let high_chip = *chips.iter().max().unwrap();
        let (low_target, low, high_target, high) = compare_instructions.get(&bot).unwrap();
        if low_target == "bot" {
            bots.entry(*low).or_insert(Vec::new()).push(low_chip);
        } else {
            outputs.insert(low, low_chip);
        }
        if high_target == "bot" {
            bots.entry(*high).or_insert(Vec::new()).push(high_chip);
        } else {
            outputs.insert(high, high_chip);
        }
        bots.remove(&bot);
        if part1_result == 0 && low_chip == LOW_VALUE && high_chip == HIGH_VALUE {
            part1_result = bot;
        }
        if part2_result == 0
            && target_outputs
                .iter()
                .all(|output| outputs.contains_key(output))
        {
            part2_result = target_outputs.iter().fold(1, |acc, output| acc * outputs[output]);
        }
    }
    (part1_result, part2_result)
}

fn get_input(file_path: &String) -> (Vec<ValueInstruction>, HashMap<u32, CompareInstruction>) {
    let value_regex = Regex::new(r"^value\s(?P<value>\d+)\sgoes to bot\s(?P<bot>\d+)$").unwrap();
    let compare_regex = Regex::new(r"^bot\s(?P<bot>\d+)\sgives low to\s(?P<lowTarget>bot|output)\s(?P<low>\d+)\sand high to\s(?P<highTarget>bot|output)\s(?P<high>\d+)$").unwrap();
    let mut value_instructions = Vec::new();
    let mut compare_instructions = HashMap::new();
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        if let Some(cap) = value_regex.captures(line) {
            value_instructions.push((
                cap.name("bot").unwrap().as_str().parse().unwrap(),
                cap.name("value").unwrap().as_str().parse().unwrap(),
            ))
        }
        if let Some(cap) = compare_regex.captures(line) {
            compare_instructions.insert(
                cap.name("bot").unwrap().as_str().parse::<u32>().unwrap(),
                (
                    String::from(cap.name("lowTarget").unwrap().as_str()),
                    cap.name("low").unwrap().as_str().parse().unwrap(),
                    String::from(cap.name("highTarget").unwrap().as_str()),
                    cap.name("high").unwrap().as_str().parse().unwrap(),
                ),
            );
        }
    }
    (value_instructions, compare_instructions)
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
