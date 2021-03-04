use std::env;
use std::fs;
use std::time::Instant;

fn is_password_valid(password: &str, check2: bool) -> bool {
    let chars = password.chars().collect::<Vec<char>>();
    if (0..chars.len() - 1).all(|index| chars[index] <= chars[index + 1]) {
        let counts = password
            .chars()
            .collect::<std::collections::HashSet<char>>()
            .iter()
            .map(|c| password.matches(*c).count())
            .collect::<Vec<usize>>();
        return (!check2 || counts.contains(&2)) && counts.iter().any(|count| *count > 1);
    }
    false
}

fn get_valid_password_count(limits: &(u32, u32), check2: bool) -> usize {
    let (start, end) = limits;
    (*start..*end)
        .filter(|password| is_password_valid(&(password.to_string()), check2))
        .count()
}

fn solve(limits: &(u32, u32)) -> (usize, usize) {
    (
        get_valid_password_count(limits, false),
        get_valid_password_count(limits, true),
    )
}

fn get_input(file_path: &String) -> (u32, u32) {
    let split: Vec<String> = fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .split("-")
        .map(|s| String::from(s))
        .collect();
    (split[0].parse().unwrap(), split[1].parse().unwrap())
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
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}
