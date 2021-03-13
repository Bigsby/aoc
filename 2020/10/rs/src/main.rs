fn part1(adapters: &Vec<u64>) -> usize {
    let mut diff1 = 0;
    let mut diff3 = 1;
    let mut current_joltage = 0;
    for joltage in adapters {
        match joltage - current_joltage {
            1 => diff1 += 1,
            3 => diff3 += 1,
            _ => (),
        }
        current_joltage = *joltage;
    }
    diff1 * diff3
}

fn calculate_combinations(sequence: u64) -> u64 {
    match sequence {
        0..=2 => 1,
        3 => 2,
        _ => {
            calculate_combinations(sequence - 1)
                + calculate_combinations(sequence - 2)
                + calculate_combinations(sequence - 3)
        }
    }
}

fn part2(adapters: &Vec<u64>) -> u64 {
    let mut adapters = adapters.clone();
    adapters.push(*adapters.iter().last().unwrap());
    let mut sequences = Vec::new();
    let mut current_sequence_length = 1;
    let mut current_joltage = 0;
    for joltage in adapters {
        if current_joltage == joltage - 1 {
            current_sequence_length += 1;
        } else {
            sequences.push(current_sequence_length);
            current_sequence_length = 1;
        }
        current_joltage = joltage;
    }
    sequences
        .into_iter()
        .fold(1u64, |acc, length| acc * calculate_combinations(length))
}

fn solve(adapters: &Vec<u64>) -> (usize, u64) {
    let mut adapters = adapters.clone();
    adapters.sort_by_key(|adapter| *adapter);
    (part1(&adapters), part2(&adapters))
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
