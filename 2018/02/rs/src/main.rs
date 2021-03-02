use std::env;
use std::fs;
use std::time::{Instant};
use itertools::Itertools;

fn part1(ids: &Vec<String>) -> usize {
    let mut twice_count = 0;
    let mut thrice_count = 0;
    for id in ids {
        let id_counts: Vec<usize> = id.chars().map(|c| id.matches(c).count()).collect();
        if id_counts.contains(&2) {
            twice_count += 1;
        }
        if id_counts.contains(&3) {
            thrice_count += 1;
        }
    }
    twice_count * thrice_count
}

fn part2(ids: &Vec<String>) -> String {
    for combination in ids.iter().combinations(2) {
        let id1 = combination[0];
        let id2 = combination[1];
        let differences: Vec<usize> = (0..id1.len())
            .filter(|index| id1.chars().nth(*index) != id2.chars().nth(*index))
            .collect();
        if differences.len() == 1 {
            let difference_index = differences[0];
            return id1.chars().take(difference_index).chain(id1.chars().skip(difference_index + 1)).collect();
        }
    }
    panic!("Ids differencing 1 not found");
}

fn solve(ids: &Vec<String>) -> (usize, String) {
    (part1(ids), part2(ids))
}

fn get_input(file_path: &String) -> Vec<String> {
    fs::read_to_string(file_path).expect("Error reading input file!")
        .lines().map(|line| String::from(line)).collect()
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:?}", now.elapsed().as_secs_f32());
}