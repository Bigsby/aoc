use std::collections::HashSet;

fn part2(changes: &Vec<i32>) -> i32 {
    let changes_length = changes.len();
    let mut frequency = 0;
    let mut previous = HashSet::new();
    let mut index = 0;
    while previous.insert(frequency) {
        frequency += changes[index];
        index = (index + 1) % changes_length;
    };
    frequency
}

fn solve(changes: &Vec<i32>) -> (i32, i32) {
    (changes.iter().sum(), part2(changes))
}

fn get_input(file_path: &String) -> Vec<i32> {
    std::fs::read_to_string(file_path).expect("Error reading input file!").split("\n")
        .map(|line| line.parse().expect(&format!("Unable to parse '{}'", line))).collect()
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