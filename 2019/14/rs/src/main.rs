use regex::Regex;
use std::collections::HashMap;

type ChemicalPortion = (u64, u32);
const FUEL: u32 = 0;
const ORE: u32 = 1;

fn calculate_required_ore(
    reactions: &HashMap<u32, (u64, Vec<ChemicalPortion>)>,
    required_fuel: u64,
) -> u64 {
    let mut required_chemicals = Vec::new();
    required_chemicals.push((FUEL, required_fuel));
    let mut produced_chemicals = HashMap::new();
    let mut ore_count = 0;
    while let Some((item, amount)) = required_chemicals.pop() {
        if amount <= *produced_chemicals.entry(item).or_insert(0) {
            *produced_chemicals.entry(item.clone()).or_insert(0) -= amount;
            continue;
        }
        let amount_needed = amount - *produced_chemicals.entry(item).or_insert(0);
        produced_chemicals.remove_entry(&item.clone());
        let (amount_produced, portions) = reactions.get(&item).unwrap();
        let required_quantity = f64::ceil(amount_needed as f64 / *amount_produced as f64) as u64;
        *produced_chemicals.entry(item).or_insert(0) +=
            (required_quantity * amount_produced) - amount_needed;
        for (other_amount_required, chemical) in portions {
            let chemical_value = other_amount_required * required_quantity;
            if *chemical == ORE {
                ore_count += chemical_value;
            } else {
                let mut requirement = chemical_value;
                if let Some((_, current_requirement)) = required_chemicals
                    .iter()
                    .filter(|(i, _)| i == chemical)
                    .next()
                {
                    requirement += *current_requirement;
                }
                required_chemicals.retain(|(i, _)| i != chemical);
                required_chemicals.push((*chemical, requirement));
            }
        }
    }
    ore_count
}

fn part2(reactions: &HashMap<u32, (u64, Vec<ChemicalPortion>)>) -> u64 {
    let mut required_fuel = 1;
    let mut last_needed = calculate_required_ore(reactions, required_fuel);
    let max_ore = u64::pow(10, 12);
    loop {
        required_fuel = required_fuel * max_ore / last_needed;
        let ore_needed = calculate_required_ore(reactions, required_fuel);
        if last_needed == ore_needed {
            break;
        } else {
            last_needed = ore_needed;
        }
    }
    required_fuel
}

fn solve(reactions: &HashMap<u32, (u64, Vec<ChemicalPortion>)>) -> (u64, u64) {
    (calculate_required_ore(reactions, 1), part2(reactions))
}

fn get_input(file_path: &String) -> HashMap<u32, (u64, Vec<ChemicalPortion>)> {
    let line_regex = Regex::new(r"(\d+)\s([A-Z]+)").unwrap();
    let mut chemicals = HashMap::new();
    chemicals.insert(String::from("FUEL"), FUEL);
    chemicals.insert(String::from("ORE"), ORE);
    let mut get_chemical_id = |name| {
        if let Some(id) = chemicals.get(&name) {
            return *id;
        } else {
            let new_id = chemicals.len() as u32;
            chemicals.insert(name, new_id);
            new_id
        }
    };
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let mut matches: Vec<regex::Captures> = line_regex.captures_iter(line).collect();
            let first = matches.pop().unwrap();
            (
                get_chemical_id(String::from(first.get(2).unwrap().as_str())),
                (
                    first.get(1).unwrap().as_str().parse().unwrap(),
                    matches
                        .into_iter()
                        .map(|cap| {
                            (
                                cap.get(1).unwrap().as_str().parse().unwrap(),
                                get_chemical_id(String::from(cap.get(2).unwrap().as_str())),
                            )
                        })
                        .collect(),
                ),
            )
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
