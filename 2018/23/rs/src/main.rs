use regex::Regex;

type Nanobot = (i64, i64, i64, i64);

fn part1(nanobots: &Vec<Nanobot>) -> usize {
    let mut max_radius = 0;
    let mut strongest_bot = (0, 0, 0, 0);
    for nanobot in nanobots {
        if nanobot.3 > max_radius {
            max_radius = nanobot.3;
            strongest_bot = *nanobot;
        }
    }
    let (x0, y0, z0, radius) = strongest_bot;
    let mut in_range = 0;
    for (x1, y1, z1, _) in nanobots {
        if (x0 - x1).abs() + (y0 - y1).abs() + (z0 - z1).abs() <= radius {
            in_range += 1;
        }
    }
    in_range
}

fn part2(nanobots: &Vec<Nanobot>) -> i64 {
    let xs: Vec<i64> = nanobots.iter().map(|bot| bot.0).collect();
    let ys: Vec<i64> = nanobots.iter().map(|bot| bot.1).collect();
    let zs: Vec<i64> = nanobots.iter().map(|bot| bot.2).collect();
    let mut xs = (*xs.iter().min().unwrap(), *xs.iter().max().unwrap());
    let mut ys = (*ys.iter().min().unwrap(), *ys.iter().max().unwrap());
    let mut zs = (*zs.iter().min().unwrap(), *zs.iter().max().unwrap());
    let mut location_radius = 1;
    while location_radius < xs.1 - xs.0 {
        location_radius *= 2;
    }
    loop {
        let mut hightest_count = 0;
        let mut best_location = (0, 0, 0);
        let mut shortest_distance = -1;
        for x in (xs.0..xs.1 + 1).step_by(location_radius as usize) {
            for y in (ys.0..ys.1 + 1).step_by(location_radius as usize) {
                for z in (zs.0..zs.1 + 1).step_by(location_radius as usize) {
                    let mut count = 0;
                    for (bot_x, bot_y, bot_z, bot_radius) in nanobots {
                        let bot_distance =
                            (x - bot_x).abs() + (y - bot_y).abs() + (z - bot_z).abs();
                        if (bot_distance - bot_radius) / location_radius <= 0 {
                            count += 1;
                        }
                    }
                    let location_distance = x.abs() + y.abs() + z.abs();
                    if count > hightest_count
                        || (count == hightest_count
                            && (shortest_distance == -1 || location_distance < shortest_distance))
                    {
                        hightest_count = count;
                        shortest_distance = location_distance;
                        best_location = (x, y, z)
                    }
                }
            }
        }
        if location_radius == 1 {
            return shortest_distance;
        } else {
            xs = (
                best_location.0 - location_radius,
                best_location.0 + location_radius,
            );
            ys = (
                best_location.1 - location_radius,
                best_location.1 + location_radius,
            );
            zs = (
                best_location.2 - location_radius,
                best_location.2 + location_radius,
            );
            location_radius /= 2;
        }
    }
}

fn solve(nanobots: &Vec<Nanobot>) -> (usize, i64) {
    (part1(nanobots), part2(nanobots))
}

fn get_input(file_path: &String) -> Vec<Nanobot> {
    let line_regex =
        Regex::new(r"pos=<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)>, r=(?P<r>-?\d+)$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    (
                        cap.name("x").unwrap().as_str().parse().unwrap(),
                        cap.name("y").unwrap().as_str().parse().unwrap(),
                        cap.name("z").unwrap().as_str().parse().unwrap(),
                        cap.name("r").unwrap().as_str().parse().unwrap(),
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
