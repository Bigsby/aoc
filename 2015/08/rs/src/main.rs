use regex::Regex;

fn get_string_difference_1(string: &String) -> usize {
    let hexa_regex = Regex::new(r"\\x[0-9a-f]{2}").unwrap();
    let total_length = string.len();
    let mut stripped = string.replace(r"\\", "r").replace("\\\"", "r");
    stripped = String::from(hexa_regex.replace_all(stripped.as_str(), "r"));
    total_length - stripped.trim_matches('"').len()
}

fn get_string_difference_2(string: &String) -> usize {
    2 + regex::escape(string).replace("\"", "\\\"").len() - string.len()
}

fn solve(strings: &Vec<String>) -> (usize, usize) {
    (
        strings.into_iter().map(get_string_difference_1).sum(),
        strings.into_iter().map(get_string_difference_2).sum(),
    )
}

fn get_input(file_path: &String) -> Vec<String> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line.trim()))
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
