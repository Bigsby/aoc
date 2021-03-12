fn part2(directions: &Vec<i32>) -> usize {
    let mut current_floor: i32 = 0;
    for (index, direction) in directions.iter().enumerate() {
        current_floor += direction;
        if current_floor == -1 {
            return index + 1;
        }
    }
    panic!("Did not go below 0!");
}

fn solve(directions: &Vec<i32>) -> (i32,usize) {
    (directions.into_iter().sum(), part2(directions))
}

fn get_input(file_path: &String) -> Vec<i32> {
    std::fs::read_to_string(file_path).expect("Error reading input file!").trim()
        .chars().map(|c| { 
            match c {
                '(' => 1,
                ')' => -1,
                _ => panic!("Unrecognized direction")
            } }).collect()
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
