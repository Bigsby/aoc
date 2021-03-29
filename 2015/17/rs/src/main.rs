use itertools::Itertools;

const TARGET_TOTAL: u32 = 150;

fn get_valid_combinations(containers: &Vec<u32>) -> Vec<usize> {
    let mut valid_combinations = Vec::new();
    for container_count in 2..containers.len() {
        for combination in containers.iter().combinations(container_count) {
            if combination.iter().map(|c| **c).sum::<u32>() == TARGET_TOTAL {
                valid_combinations.push(combination.len());
            }
        }
    }
    valid_combinations
}

fn solve(containers: &Vec<u32>) -> (usize, usize) {
    let valid_combinations = get_valid_combinations(containers);
    let min_count = valid_combinations.iter().min().unwrap();
    (
        valid_combinations.len(),
        valid_combinations
            .iter()
            .filter(|combination| *combination == min_count)
            .count(),
    )
}

fn get_input(file_path: &String) -> Vec<u32> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| line.trim().parse().unwrap())
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
