use std::collections::{HashSet, VecDeque};

type Point = (i32, i32, i32, i32);

fn solve(points: &Vec<Point>) -> (usize, String) {
    let mut edges: Vec<HashSet<usize>> = vec![HashSet::new(); points.len()];
    for (this_point, (w0, x0, y0, z0)) in points.iter().enumerate() {
        for (that_point, (w1, x1, y1, z1)) in points.iter().enumerate() {
            if (w0 - w1).abs() + (x0 - x1).abs() + (y0 - y1).abs() + (z0 - z1).abs() < 4 {
                edges[this_point].insert(that_point);
            }
        }
    }
    let mut visited = HashSet::new();
    let mut constellations = 0;
    for this_point in 0..points.len() {
        if visited.contains(&this_point) {
            continue;
        }
        constellations += 1;
        let mut queue = VecDeque::new();
        queue.push_back(this_point);
        while let Some(current_point) = queue.pop_front() {
            if visited.insert(current_point) {
                for other in &edges[current_point] {
                    queue.push_back(*other);
                }
            }
        }
    }
    (constellations, String::default())
}

fn get_input(file_path: &String) -> Vec<Point> {
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            let split = line.split(",").collect::<Vec<&str>>();
            (
                split[0].parse().unwrap(),
                split[1].parse().unwrap(),
                split[2].parse().unwrap(),
                split[3].parse().unwrap(),
            )
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
