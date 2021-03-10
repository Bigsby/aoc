fn get_next_value(value: &str) -> String {
    let mut result = String::new();
    let mut last_digit = '\0';
    let mut length = 0;
    for c in value.chars() {
        if c == last_digit {
            length += 1;
        } else {
            if last_digit != '\0' {
                result.push_str(length.to_string().as_str());
                result.push(last_digit);
            }
            last_digit = c;
            length = 1;
        }
    }
    result.push_str(length.to_string().as_str());
    result.push(last_digit);
    result
}

fn solve(puzzle_input: &str) -> (usize, usize) {
    let mut current_value = String::from(puzzle_input);
    let mut part1 = 0;
    for turn in 0..50 {
        if turn == 40 {
            part1 = current_value.len();
        }
        current_value = get_next_value(&current_value);
    }
    (part1, current_value.len())
}

fn get_input(file_path: &String) -> String {
    String::from(
        std::fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .trim(),
    )
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
