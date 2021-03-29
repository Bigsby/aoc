fn part1(steps: &usize) -> usize {
    let mut spin_lock = Vec::new();
    spin_lock.push(0);
    let mut position = 0;
    for number in 1..2017 + 1 {
        position = (position + *steps) % spin_lock.len() + 1;
        spin_lock.insert(position, number);
    }
    return spin_lock[position + 1];
}

fn part2(steps: &usize) -> usize {
    let mut position = 0;
    let mut result = 0;
    for number in 1..50_000_000 + 1 {
        position = ((position + steps) % number) + 1;
        if position == 1 {
            result = number;
        }
    }
    result
}

fn solve(steps: &usize) -> (usize, usize) {
    (part1(steps), part2(steps))
}

fn get_input(file_path: &String) -> usize {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
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
