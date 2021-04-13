type Range = (u64, u64);

fn solve(ranges: &Vec<Range>) -> (u64, u64) {
    let mut part1_result = 0;
    let mut ranges = ranges.clone();
    ranges.sort();
    let mut previous_upper = 0;
    let mut allowed_count = 0;
    for (lower, upper) in ranges {
        if upper <= previous_upper {
            continue;
        }
        if lower > previous_upper + 1 {
            allowed_count += lower - previous_upper - 1;
            if part1_result == 0 {
                part1_result = previous_upper + 1;
            }
        }
        previous_upper = upper;
    }
    (part1_result, allowed_count)
}

fn get_input(file_path: &String) -> Vec<Range> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let splits = line.trim().split("-").collect::<Vec<&str>>();
            (splits[0].parse().unwrap(), splits[1].parse().unwrap())
        })
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
