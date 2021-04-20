use regex::Regex;

const FIRST_CODE: u64 = 20151125;
const MULTIPLIER: u64 = 252533;
const DIVIDER: u64 = 33554393;

fn solve(data: &(u64, u64)) -> (u64, String) {
    let (target_row, target_column) = data;
    let mut last_code = FIRST_CODE;
    let mut current_length = 1;
    loop {
        let mut column = 0;
        current_length += 1;
        let mut row = current_length;
        while row > 0 {
            column += 1;
            last_code = (last_code * MULTIPLIER) % DIVIDER;
            if column == *target_column && row == *target_row {
                return (last_code, String::default());
            }
            row -= 1;
        }
    }
}

fn get_input(file_path: &String) -> (u64, u64) {
    Regex::new(r"row (?P<row>\d+), column (?P<column>\d+)")
        .unwrap()
        .captures(&std::fs::read_to_string(file_path).expect("Error reading input file!"))
        .map(|cap| {
            (
                cap.name("row").unwrap().as_str().parse().unwrap(),
                cap.name("column").unwrap().as_str().parse().unwrap(),
            )
        })
        .unwrap()
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
