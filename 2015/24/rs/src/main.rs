use itertools::Itertools;

fn get_minimum_group_entanglement(weights: &Vec<u64>, group_count: u64) -> u64 {
    let group_weight: u64 = weights.iter().sum::<u64>() / group_count;
    for size in 1..weights.len() {
        let entanglements: Vec<u64> = weights
            .iter()
            .copied()
            .combinations(size)
            .filter(|group| group.iter().sum::<u64>() == group_weight)
            .map(|group| group.iter().fold(1, |acc, weight| acc * weight))
            .collect();
        if !entanglements.is_empty() {
            return *entanglements.iter().min().unwrap();
        }
    }
    panic!("Group not found")
}

fn solve(weights: &Vec<u64>) -> (u64, u64) {
    (
        get_minimum_group_entanglement(weights, 3),
        get_minimum_group_entanglement(weights, 4),
    )
}

fn get_input(file_path: &String) -> Vec<u64> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| line.parse().unwrap())
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
