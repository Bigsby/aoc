fn get_checksum(data: &str, disk_length: usize) -> String {
    let mut data: Vec<char> = data.chars().collect();
    while data.len() < disk_length {
        let to_add = data
            .iter()
            .rev()
            .map(|c| if *c == '0' { '1' } else { '0' })
            .collect::<Vec<char>>();
        data.push('0');
        data.extend(to_add);
    }
    data = data.into_iter().take(disk_length).collect();
    while data.len() % 2 == 0 {
        data = (0..data.len() / 2)
            .map(|index| {
                if data[2 * index] == data[2 * index + 1] {
                    '1'
                } else {
                    '0'
                }
            })
            .collect();
    }
    return data.into_iter().collect();
}

fn solve(data: &str) -> (String, String) {
    (get_checksum(data, 272), get_checksum(data, 35651584))
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
