fn part2(number: &i32) -> usize {
    let total = number * 100 + 100_000;
    let mut non_primes = 0;
    for candidate in (total..total + 17_000 + 1).step_by(17) {
        let mut divider = 2;
        while candidate % divider != 0 {
            divider += 1;
        }
        if candidate != divider {
            non_primes += 1;
        }
    }
    non_primes
}

fn solve(number: &i32) -> (i32, usize) {
    ((number - 2).pow(2), part2(number))
}

fn get_input(file_path: &String) -> i32 {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .collect::<Vec<&str>>()[0]
        .split(" ")
        .collect::<Vec<&str>>()[2]
        .parse()
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
