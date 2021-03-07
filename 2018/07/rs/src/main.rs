use regex::Regex;
use std::collections::HashMap;

fn build_dependency_graph(pairs: &Vec<(char, char)>) -> HashMap<char, Vec<char>> {
    let mut dependencies = HashMap::new();
    for (dependency, dependant) in pairs {
        if dependencies.get(dependency).is_none() {
            dependencies.insert(*dependency, vec![]);
        }
        dependencies
            .entry(*dependant)
            .or_insert(vec![])
            .push(*dependency);
    }
    dependencies
}

fn part1(dependencies: &HashMap<char, Vec<char>>) -> String {
    let mut dependencies: HashMap<char, Vec<char>> = dependencies
        .iter()
        .map(|(step, step_dependencies)| (*step, step_dependencies.clone()))
        .collect();
    let mut path = Vec::new();
    while dependencies.len() > 0 {
        let mut next_steps: Vec<char> = dependencies
            .iter()
            .filter_map(|(step, step_dependencies)| {
                if step_dependencies.len() == 0 {
                    Some(step)
                } else {
                    None
                }
            })
            .map(|step| *step)
            .collect();
        next_steps.sort();
        let next_step = *next_steps.iter().next().unwrap();
        dependencies.remove_entry(&next_step);
        path.push(next_step);
        for step_dependencies in dependencies.values_mut() {
            if let Some(position) = step_dependencies.iter().position(|step| *step == next_step) {
                step_dependencies.remove(position);
            }
        }
    }
    path.iter().collect::<String>()
}

fn part2(dependencies: &HashMap<char, Vec<char>>) -> usize {
    let mut dependencies: HashMap<char, Vec<char>> = dependencies
        .iter()
        .map(|(step, step_dependencies)| (*step, step_dependencies.clone()))
        .collect();
    let worker_count = 5;
    let step_duration_offset: u32 = ('A' as u32) - 60 - 1;
    let mut running_workers: HashMap<char, u32> = HashMap::new();
    let mut seconds = 0;
    while dependencies.len() > 0 || running_workers.len() > 0 {
        let mut to_remove = Vec::new();
        for (step, remaining) in &running_workers {
            if remaining == &1 {
                to_remove.push(*step);
            }
        }
        running_workers = running_workers
            .into_iter()
            .filter_map(|(step, remaining)| {
                if remaining == 1 {
                    None
                } else {
                    Some((step, remaining - 1))
                }
            })
            .collect();

        for step in to_remove {
            for step_dependencies in dependencies.values_mut() {
                if let Some(position) = step_dependencies
                    .iter()
                    .position(|dependency_step| dependency_step == &step)
                {
                    step_dependencies.remove(position);
                }
            }
        }
        let mut next_steps = dependencies
            .iter()
            .filter_map(|(step, step_dependencies)| {
                if step_dependencies.len() == 0 {
                    Some(step)
                } else {
                    None
                }
            })
            .map(|step| *step)
            .collect::<Vec<char>>();
        next_steps.sort();
        let mut next_steps = next_steps.iter();
        let mut next_step = next_steps.next();
        while running_workers.len() < worker_count && !next_step.is_none() {
            running_workers.insert(
                *next_step.unwrap(),
                (*next_step.unwrap() as u32) - step_duration_offset,
            );

            dependencies.remove_entry(next_step.unwrap());
            next_step = next_steps.next();
        }
        seconds += 1;
    }
    seconds - 1
}

fn solve(pairs: &Vec<(char, char)>) -> (String, usize) {
    let dependencies = build_dependency_graph(pairs);
    (part1(&dependencies), part2(&dependencies))
}

fn get_input(file_path: &String) -> Vec<(char, char)> {
    let re = Regex::new(r"\s([A-Z])\s").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let caps: Vec<&str> = re
                .captures_iter(line)
                .map(|cap| cap.get(1).unwrap().as_str())
                .collect();
            return (
                caps[0].chars().next().unwrap(),
                caps[1].chars().next().unwrap(),
            );
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
