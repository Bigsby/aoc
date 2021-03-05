use std::collections::HashMap;

type Group = (u32, Vec<u32>);

fn solve(groups: &Vec<Group>) -> (usize, usize) {
    (
        groups.iter().map(|(_, answers)| answers.len()).sum(),
        groups
            .iter()
            .map(|(people_count, anwsers)| {
                anwsers
                    .iter()
                    .filter(|count| *count == people_count)
                    .count()
            })
            .sum(),
    )
}

fn get_input(file_path: &String) -> Vec<Group> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("\n\n")
        .map(|entry| {
            let mut answers = HashMap::new();
            let mut people_count = 0;
            for line in entry.lines() {
                if !line.trim().is_empty() {
                    people_count += 1;
                }
                for c in line.chars() {
                    *answers.entry(c).or_insert(0) += 1;
                }
            }
            (
                people_count,
                answers
                    .values()
                    .map(|count| *count)
                    .collect::<Vec<u32>>()
                    .clone(),
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", end);
}
