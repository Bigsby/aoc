type Instruction = Vec<String>;

fn solve(instructions: &Vec<Instruction>) -> (usize, String) {
    let target: usize =
        instructions[1][1].parse::<usize>().unwrap() * instructions[2][1].parse::<usize>().unwrap();
    let mut a = 1;
    while a < target {
        if a % 2 == 0 {
            a = a * 2 + 1;
        } else {
            a *= 2;
        }
    }
    return (a - target, String::default());
}

fn get_input(file_path: &String) -> Vec<Instruction> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| line.split(" ").map(|s| String::from(s)).collect())
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
