static PATTERN: [i16; 4] = [0, 1, 0, -1];

fn get_value(offset: usize, signal: &Vec<i16>) -> i16 {
    let mut total = 0;
    for (index, number) in signal.into_iter().enumerate() {
        total += number * PATTERN[((index + 1) / offset) % PATTERN.len()];
    }
    i16::abs(total) % 10
}

fn next_phase(signal: &Vec<i16>) -> Vec<i16> {
    let mut result = Vec::new();
    for index in 0..signal.len() {
        result.push(get_value(index + 1, signal));
    }
    result
}

fn part1(signal: &Vec<i16>) -> String {
    let mut signal = signal.clone();
    for _ in 0..100 {
        signal = next_phase(&signal);
    }
    signal
        .into_iter()
        .take(8)
        .map(|i| (i as u8 + 48) as char)
        .collect()
}

fn part2(signal: &Vec<i16>) -> String {
    let offset = signal
        .iter()
        .take(7)
        .map(|i| (*i as u8 + 48) as char)
        .collect::<String>()
        .parse()
        .unwrap();
    let mut signal: Vec<i16> = signal
        .iter()
        .cycle()
        .take(10_000 * signal.len())
        .skip(offset)
        .map(|i| *i)
        .collect();
    for _ in 0..100 {
        let mut sum = 0;
        for index in (0..signal.len()).rev() {
            sum = (sum + signal[index]) % 10;
            signal[index] = sum;
        }
    }
    signal
        .into_iter()
        .take(8)
        .map(|i| (i as u8 + 48) as char)
        .collect()
}

fn solve(puzzle_input: &Vec<i16>) -> (String, String) {
    (part1(puzzle_input), part2(puzzle_input))
}

fn get_input(file_path: &String) -> Vec<i16> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .chars()
        .map(|c| (c as i8 - 48) as i16)
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
