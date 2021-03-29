use num::Complex;
use std::collections::VecDeque;

static DIRECTIONS: &'static [(char, Complex<i32>)] = &[
    ('U', Complex::new(0, 1)),
    ('D', Complex::new(0, -1)),
    ('L', Complex::new(-1, 0)),
    ('R', Complex::new(1, 0)),
];

fn solve(passcode: &str) -> (String, usize) {
    let mut queue = VecDeque::new();
    const TARGET_ROOM: Complex<i32> = Complex::new(3, -3);
    queue.push_back((Complex::new(0, 0), String::from("")));
    let mut longest_path_found = 0;
    let mut shortest_path = String::default();
    while let Some((room, path)) = queue.pop_front() {
        if room == TARGET_ROOM {
            longest_path_found = longest_path_found.max(path.len());
            if shortest_path == String::default() {
                shortest_path = String::from(path.clone());
            }
            continue;
        }
        let path_hash = format!("{:x}", md5::compute(format!("{}{}", passcode, path)));
        for (index, (path_letter, direction)) in DIRECTIONS.into_iter().enumerate() {
            let new_room = room + direction;
            if path_hash.chars().into_iter().nth(index).unwrap() > 'a'
                && new_room.re >= 0
                && new_room.re < 4
                && new_room.im <= 0
                && new_room.im > -4
            {
                let mut new_path = path.clone();
                new_path.push(*path_letter);
                queue.push_back((new_room, new_path));
            }
        }
    }

    (shortest_path, longest_path_found)
}

fn get_input(file_path: &String) -> String {
    String::from(
        std::fs::read_to_string(file_path)
            .expect("Error reading input file!")
            .trim(),
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
