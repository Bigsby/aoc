type Tiles = Vec<bool>;

fn solve(tiles: &Tiles) -> (usize, usize) {
    let mut safe = tiles.iter().filter(|tile| **tile).count();
    let mut part1_result = 0;
    let mut tiles = tiles.clone();
    let tile_count = tiles.len();
    for step in 1..400_000 {
        if step == 40 {
            part1_result = safe;
        }
        tiles = (0..tile_count)
            .into_iter()
            .map(|index| {
                (index == 0 || *tiles.iter().nth(index - 1).unwrap())
                    == (index == tile_count - 1 || *tiles.iter().nth(index + 1).unwrap())
            })
            .collect();
        safe += tiles.iter().filter(|tile| **tile).count();
    }
    (part1_result, safe)
}

fn get_input(file_path: &String) -> Tiles {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .trim()
        .chars()
        .map(|c| c == '.')
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
