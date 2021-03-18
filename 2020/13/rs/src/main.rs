#[derive(Debug)]
struct Bus {
    id: i64,
    index: i64,
}

fn part1(puzzle_input: &(i64, Vec<Bus>)) -> i64 {
    let (timestamp, busses) = puzzle_input;
    let mut closest_after = i64::MAX;
    let mut closest_id = 0;
    for bus in busses {
        let time_after = (timestamp / bus.id + 1) * bus.id - timestamp;
        if time_after < closest_after {
            closest_after = time_after;
            closest_id = bus.id;
        }
    }
    closest_after * closest_id
}

fn modular_multiplicative_inverse(a: i64, b: i64) -> i64 {
    let q = a % b;
    for i in 1..b {
        if (q * i) % b == 1 {
            return i;
        }
    }
    return 1;
}

fn absolute_modulo(a: i64, n: i64) -> i64 {
    ((a % n) + n) % n
}

fn part2(puzzle_input: &(i64, Vec<Bus>)) -> i64 {
    let (_, busses) = puzzle_input;
    let product = busses.into_iter().fold(1, |acc, bus| acc * bus.id);
    let mut sum = 0;
    for bus in busses {
        let current_product = product / bus.id;
        sum += absolute_modulo(bus.id - bus.index, bus.id)
            * current_product
            * modular_multiplicative_inverse(current_product, bus.id);
    }
    sum % product
}

fn solve(puzzle_input: &(i64, Vec<Bus>)) -> (i64, i64) {
    (part1(puzzle_input), part2(puzzle_input))
}

fn get_input(file_path: &String) -> (i64, Vec<Bus>) {
    let lines: Vec<String> = std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| String::from(line))
        .collect();
    (
        lines[0].trim().parse().unwrap(),
        lines[1]
            .split(",")
            .enumerate()
            .filter(|(_, id)| *id != "x")
            .map(|(index, id)| Bus {
                id: id.parse().unwrap(),
                index: index as i64,
            })
            .collect(),
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
    println!("P2: {}", part2_result);
    println!();
    println!("Time: {:.7}", end);
}
