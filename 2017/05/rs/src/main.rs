fn do_jumps<T>(jumps: &Vec<i32>, new_jump_junc: T) -> i32
where
    T: Fn(i32) -> i32,
{
    let mut jumps = jumps.clone();
    let max_index = jumps.len() as i32;
    let mut index = 0i32;
    let mut count = 0;
    while index >= 0 && index < max_index {
        count += 1;
        let offset = jumps[index as usize];
        let next_index = index + offset;
        jumps[index as usize] = offset + new_jump_junc(offset);
        index = next_index;
    }
    count
}

fn solve(jumps: &Vec<i32>) -> (i32, i32) {
    (
        do_jumps(jumps, |_| 1),
        do_jumps(jumps, |offset| if offset < 3 { 1 } else { -1 }),
    )
}

fn get_input(file_path: &String) -> Vec<i32> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| line.parse().unwrap())
        .collect()
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() != 2 {
        panic!("Please, add input file path as parameter");
    }
    let now = std::time::Instant::now();
    let (part1_result, part2_result) = solve(&get_input(&args[1]));
    println!("P1: {}", part1_result);
    println!("P1: {}", part2_result);
    println!();
    println!("Time: {:7}", now.elapsed().as_secs_f32());
}
