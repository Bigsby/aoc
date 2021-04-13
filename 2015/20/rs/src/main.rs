fn get_divisors(number: i32) -> Vec<i32> {
    let mut result = Vec::new();
    let mut large_divisors = Vec::new();
    for i in 1..(number as f32).sqrt() as i32 + 1 {
        if number % i == 0 {
            result.push(i);
            if i * i != number {
                large_divisors.push(number / i);
            }
        }
    }
    large_divisors.reverse();
    for divisor in large_divisors {
        result.push(divisor);
    }
    result
}

fn get_present_count_for_house(number: i32) -> i32 {
    get_divisors(number).iter().sum()
}

fn part1(puzzle_input: &i32) -> i32 {
    let mut house_number = 0;
    let mut presents_received = 0;
    let step = 2 * 3 * 5 * 7 * 11;
    let target_presents = puzzle_input / 10;
    while presents_received <= target_presents {
        house_number += step;
        presents_received = get_present_count_for_house(house_number);
    }
    house_number
}

fn get_present_count_for_house2(number: i32) -> i32 {
    let mut presents = 0;
    for divisor in get_divisors(number) {
        if number / divisor < 50 {
            presents += divisor * 11;
        }
    }
    presents
}

fn part2(puzzle_input: &i32, house_number: i32) -> i32 {
    let mut house_number = house_number;
    let mut presents_received = 0;
    while presents_received <= *puzzle_input {
        house_number += 1;
        presents_received = get_present_count_for_house2(house_number);
    }
    house_number
}

fn solve(puzzle_input: &i32) -> (i32, i32) {
    let part1_result = part1(puzzle_input);
    (part1_result, part2(puzzle_input, part1_result))
}

fn get_input(file_path: &String) -> i32 {
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
