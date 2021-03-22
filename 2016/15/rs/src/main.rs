use regex::Regex;

#[derive(Copy, Clone)]
struct Disc {
    positions: u32,
    offset: u32,
}

impl Disc {
    fn new(positions: u32, start: u32, index: u32) -> Disc {
        Disc {
            positions,
            offset: start + index + 1,
        }
    }
}

fn find_winning_position(discs: &Vec<Disc>) -> u32 {
    let mut jump = 1;
    let mut offset = 0;
    for disc in discs {
        while (offset + disc.offset) % disc.positions != 0 {
            offset += jump;
        }
        jump *= disc.positions;
    }
    offset
}

fn solve(discs: &Vec<Disc>) -> (u32, u32) {
    let part1_result = find_winning_position(discs);
    let mut discs: Vec<Disc> = discs.into_iter().map(|disc| *disc).collect();
    discs.push(Disc::new(11, 0, discs.len() as u32));
    (part1_result, find_winning_position(&discs))
}

fn get_input(file_path: &String) -> Vec<Disc> {
    let line_regex = Regex::new(
        r"^Disc #\d has (?P<positions>\d+) positions; at time=0, it is at position (?P<start>\d+).$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
        .map(|(index, line)| {
            line_regex
                .captures(line)
                .map(|cap| {
                    Disc::new(
                        cap.name("positions").unwrap().as_str().parse().unwrap(),
                        cap.name("start").unwrap().as_str().parse().unwrap(),
                        index as u32,
                    )
                })
                .unwrap()
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
