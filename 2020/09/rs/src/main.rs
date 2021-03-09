fn has_no_valid_pair(number_index: usize, numbers: &Vec<u64>) -> bool {
    let number = numbers[number_index];
    for test_index in (number_index - 25)..number_index {
        let test_number = numbers[test_index];
        for pair_index in (number_index - 25)..number_index {
            if pair_index != test_index && test_number + numbers[pair_index] == number {
                return false;
            }
        }
    }
    true
}

fn get_weakness(numbers: &Vec<u64>, target_number: u64) -> u64 {
    for start_index in 0..numbers.len() {
        let mut current_sum = 0;
        let mut length = 1;
        while current_sum < target_number {
            let new_set: Vec<&u64> = numbers[start_index..start_index + length]
                .into_iter()
                .collect();
            current_sum = new_set.iter().map(|i| *i).sum();
            if current_sum == target_number {
                return *new_set.iter().min().unwrap() + *new_set.iter().max().unwrap();
            }
            length += 1;
        }
    }
    panic!("Weakness not found")
}

fn solve(numbers: &Vec<u64>) -> (u64, u64) {
    let part1_result = numbers[(25..numbers.len())
        .into_iter()
        .filter(|index| has_no_valid_pair(*index, numbers))
        .next()
        .unwrap()];
    (part1_result, get_weakness(numbers, part1_result))
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
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
