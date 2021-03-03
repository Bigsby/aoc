use std::env;
use std::fs;
use std::time::Instant;

fn find_hash(secret_key: &str, prefix_count: u32, guess: u32) -> u32 {
    let prefix = (0..prefix_count).map(|_| "0").collect::<String>();
    let mut guess = guess;
    loop {
        let hash = format!("{:x}", md5::compute(format!("{}{}", secret_key, guess)));
        if hash.starts_with(&prefix) {
            return guess;
        }
        guess += 1;
    }
}

fn solve(secret_key: &str) -> (u32, u32) {
    let part1_result = find_hash(secret_key, 5, 1);
    (part1_result, find_hash(secret_key, 6, part1_result))
}

fn get_input(file_path: &String) -> String {
    String::from(
        fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .trim(),
    )
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
