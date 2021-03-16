use itertools::Itertools;
use regex::Regex;
use std::collections::{HashMap, HashSet};

type Entry = (u32, u32, i32);
type Entries = Vec<Entry>;

fn get_hapinness(target: u32, other: u32, entries: &Entries) -> i32 {
    entries
        .into_iter()
        .filter(|entry| entry.0 == target && entry.1 == other)
        .next()
        .unwrap()
        .2
}

fn calculate_happiness(arrangement: &Vec<u32>, entries: &Entries) -> i32 {
    let mut total = 0;
    let length = arrangement.len();
    for (index, person) in arrangement.into_iter().enumerate() {
        total += get_hapinness(
            *person,
            arrangement[if index == 0 { length - 1 } else { index - 1 }],
            entries,
        );
        total += get_hapinness(*person, arrangement[(index + 1) % length], entries);
    }
    total
}

fn calculate_maximum_happiness(possible_arragements: &Vec<Vec<u32>>, entries: &Entries) -> i32 {
    possible_arragements
        .into_iter()
        .map(|arrangement| calculate_happiness(arrangement, entries))
        .max()
        .unwrap()
}

fn part1(entries: &Entries) -> i32 {
    let people: Vec<u32> = entries
        .iter()
        .map(|entry| entry.0)
        .collect::<HashSet<_>>()
        .into_iter()
        .collect();
    let people_count = people.len();
    calculate_maximum_happiness(
        &people.into_iter().permutations(people_count).collect(),
        entries,
    )
}

fn part2(entries: &Entries) -> i32 {
    let mut entries: Entries = entries.clone();
    let people: Vec<u32> = entries
        .iter()
        .map(|entry| entry.0)
        .collect::<HashSet<_>>()
        .into_iter()
        .collect();
    let me = people.len() as u32;
    for person in people {
        entries.push((me, person, 0));
        entries.push((person, me, 0));
    }
    part1(&entries)
}

fn solve(entries: &Entries) -> (i32, i32) {
    (part1(entries), part2(entries))
}

fn get_input(file_path: &String) -> Entries {
    let line_regex = Regex::new(
        r"^(\w+)\swould\s(gain|lose)\s(\d+)\shappiness\sunits\sby\ssitting\snext\sto\s(\w+)\.$",
    )
    .unwrap();
    let mut people: HashMap<String, u32> = HashMap::new();
    let mut next_id = 0;
    let mut get_person_id = |name: &str| {
        if !people.contains_key(name) {
            people.insert(String::from(name), next_id);
            next_id += 1;
        }
        *people.get(name).unwrap()
    };
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    let target = get_person_id(cap.get(1).unwrap().as_str());
                    let other = get_person_id(cap.get(4).unwrap().as_str());
                    (
                        target,
                        other,
                        (if cap.get(2).unwrap().as_str() == "gain" {
                            1
                        } else {
                            -1
                        }) * cap.get(3).unwrap().as_str().parse::<i32>().unwrap(),
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
