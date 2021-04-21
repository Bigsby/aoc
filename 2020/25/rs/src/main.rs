const BASE_SUBJECT_NUMBER: u64 = 7;
const DIVIDER: u64 = 20201227;

fn get_next_value(value: u64, subject_number: u64) -> u64 {
    (value * subject_number) % DIVIDER
}

fn get_loop_size(target: u64) -> u64 {
    let mut value = 1;
    let mut cycle = 0;
    while value != target {
        cycle += 1;
        value = get_next_value(value, BASE_SUBJECT_NUMBER)
    }
    cycle
}

fn transform(subject_number: u64, cycles: u64) -> u64 {
    let mut value = 1;
    let mut cycles = cycles;
    while cycles > 0 {
        cycles -= 1;
        value = get_next_value(value, subject_number);
    }
    value
}

fn solve(puzzle_input: &(u64, u64)) -> (u64, String) {
    let (card, door) = puzzle_input;
    (transform(*card, get_loop_size(*door)), String::default())
}

fn get_input(file_path: &String) -> (u64, u64) {
    let lines: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|s| String::from(s))
        .collect();
    (lines[0].parse().unwrap(), lines[1].parse().unwrap())
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
