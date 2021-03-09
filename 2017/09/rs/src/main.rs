const GROUP_START: char = '{';
const GROUP_END: char = '}';
const GARBAGE_START: char = '<';
const GARBAGE_END: char = '>';
const ESCAPE: char = '!';

fn solve(stream: &str) -> (u32, u32) {
    let mut group_score = 0;
    let mut garbage_count = 0;
    let mut depth = 0;
    let mut in_garbage = false;
    let mut escape = false;
    for c in stream.chars() {
        if escape {
            escape = false;
        } else if in_garbage {
            if c == ESCAPE {
                escape = true;
            } else if c == GARBAGE_END {
                in_garbage = false;
            } else {
                garbage_count += 1;
            }
        } else if c == GARBAGE_START {
            in_garbage = true;
        } else if c == GROUP_START {
            depth += 1;
        } else if c == GROUP_END {
            group_score += depth;
            depth -= 1;
        }
    }
    (group_score, garbage_count)
}

fn get_input(file_path: &String) -> String {
    String::from(std::fs::read_to_string(file_path).expect("Error reading input file!"))
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
