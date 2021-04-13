use regex::Regex;
use std::collections::{HashMap, HashSet};

type Values = [i32; 3];
type Particle = (Values, Values, Values);

fn get_manhatan_value(values: &Values) -> i32 {
    values[0].abs() + values[1].abs() + values[2].abs()
}

fn part1(particles: &Vec<Particle>) -> usize {
    let mut closest_particle = 0;
    let mut lowest_acceleration = i32::MAX;
    let mut lowest_position = i32::MAX;
    for (index, (position, _, acceleration)) in particles.into_iter().enumerate() {
        let acceleration_total = get_manhatan_value(acceleration);
        if acceleration_total < lowest_acceleration {
            lowest_acceleration = acceleration_total;
            closest_particle = index;
            lowest_position = get_manhatan_value(position);
        }
        if acceleration_total == lowest_acceleration
            && get_manhatan_value(position) < lowest_position
        {
            closest_particle = index;
            lowest_position = get_manhatan_value(position);
        }
    }
    closest_particle
}

fn get_quadratic_abc(
    particle_a: &Particle,
    particle_b: &Particle,
    coordinate: usize,
) -> (f32, f32, f32) {
    let p_a_p = particle_a.0[coordinate] as f32;
    let p_a_a = particle_a.2[coordinate] as f32;
    let p_a_v = particle_a.1[coordinate] as f32 + p_a_a / 2.0;
    let p_b_p = particle_b.0[coordinate] as f32;
    let p_b_a = particle_b.2[coordinate] as f32;
    let p_b_v = particle_b.1[coordinate] as f32 + p_b_a / 2.0;
    ((p_a_a - p_b_a) / 2.0, p_a_v - p_b_v, p_a_p - p_b_p)
}

fn get_colition_times(particle_a: &Particle, particle_b: &Particle) -> Vec<i32> {
    let (a, b, c) = get_quadratic_abc(particle_a, particle_b, 0);
    let mut times = Vec::new();
    if a == 0.0 {
        if b != 0.0 {
            times.push(-c / b);
        }
    } else {
        let bb = b * b;
        let ac4 = a * c * 4.0;
        if bb < ac4 {
            return vec![];
        } else if bb == ac4 {
            times.push(-b / (2.0 * a));
        } else {
            let rt = (bb - ac4).sqrt();
            times.push((-b + rt) / (2.0 * a));
            times.push((-b - rt) / (2.0 * a));
        }
    }
    let int_times: Vec<f32> = times
        .into_iter()
        .filter(|t| *t >= 0.0 && t.fract() == 0.0)
        .collect();
    let mut result = Vec::new();
    for t in int_times {
        let mut collide = true;
        for k in 1..3 {
            let (a, b, c) = get_quadratic_abc(particle_a, particle_b, k);
            if a * t * t + b * t + c != 0.0 {
                collide = false;
                break;
            }
        }
        if collide {
            result.push(t as i32);
        }
    }
    result
}

fn part2(particles: &Vec<Particle>) -> usize {
    let mut collisions = HashMap::new();
    for this_index in 0..particles.len() - 1 {
        for other_index in this_index + 1..particles.len() {
            for time in get_colition_times(&particles[this_index], &particles[other_index]) {
                collisions
                    .entry(time)
                    .or_insert(Vec::new())
                    .push((this_index, other_index));
            }
        }
    }
    let mut particle_indexes = (0..particles.len()).into_iter().collect::<HashSet<usize>>();
    let mut times = collisions.keys().collect::<Vec<&i32>>();
    times.sort();
    for time in times {
        let mut collided_to_remove = HashSet::new();
        for (index_a, index_b) in collisions.get(time).unwrap() {
            if particle_indexes.contains(index_a) && particle_indexes.contains(index_b) {
                collided_to_remove.insert(*index_a);
                collided_to_remove.insert(*index_b);
            }
        }
        particle_indexes = particle_indexes
            .difference(&collided_to_remove)
            .map(|i| *i)
            .collect();
    }
    particle_indexes.len()
}

fn solve(particles: &Vec<Particle>) -> (usize, usize) {
    (part1(particles), part2(particles))
}

fn parse_values(text: &str) -> Values {
    let split = text.trim().split(",").collect::<Vec<&str>>();
    [
        split[0].parse().unwrap(),
        split[1].parse().unwrap(),
        split[2].parse().unwrap(),
    ]
}

fn get_input(file_path: &String) -> Vec<Particle> {
    let line_regex = Regex::new(r"^p=<(?P<p>[^>]+)>, v=<(?P<v>[^>]+)>, a=<(?P<a>[^>]+)>$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    (
                        parse_values(cap.name("p").unwrap().as_str()),
                        parse_values(cap.name("v").unwrap().as_str()),
                        parse_values(cap.name("a").unwrap().as_str()),
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
