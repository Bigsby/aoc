
fn part1(puzzle_input: &str) -> usize {
    puzzle_input.len()
}

fn part2(puzzle_input: &str) -> usize {
    puzzle_input.len()
}

fn solve(puzzle_input: &str) -> (usize,usize) {
    (part1(puzzle_input), part2(puzzle_input))
}

fn get_input(file_path: &String) -> String {
    std::fs::read_to_string(file_path).expect("Error reading input file!")
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
