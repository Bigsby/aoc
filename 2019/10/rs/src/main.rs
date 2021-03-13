use num::complex::Complex;

type Asteroid = Complex<i32>;

fn get_visible_count(asteroid: Asteroid, asteroids: &Vec<Asteroid>, max_x: i32, max_y: i32) -> u32 {
    let mut asteroids = asteroids.clone();
    let mut removed = Vec::new();
    removed.push(asteroid);
    let mut visible_count = 0;
    while let Some(asteroid_to_check) = asteroids.pop() {
        if removed.contains(&asteroid_to_check) {
            continue;
        }
        visible_count += 1;
        let delta = asteroid_to_check - asteroid;
        let jump = delta / num::integer::gcd(i32::abs(delta.re), i32::abs(delta.im));
        let mut asteroid_to_check = asteroid + jump;
        while asteroid_to_check.re >= 0
            && asteroid_to_check.re <= max_x
            && asteroid_to_check.im >= 0
            && asteroid_to_check.im <= max_y
        {
            removed.push(asteroid_to_check);
            asteroid_to_check += jump;
        }
    }
    visible_count
}

fn part1(asteroids: &Vec<Asteroid>) -> (u32, Asteroid) {
    let max_x = asteroids
        .into_iter()
        .map(|asteroid| asteroid.re)
        .max()
        .unwrap();
    let max_y = asteroids
        .into_iter()
        .map(|asteroid| asteroid.im)
        .max()
        .unwrap();
    let mut max_visible_count = 0;
    let mut monitoring_station = Asteroid::new(-1, -1);
    for asteroid in asteroids {
        let visible_count = get_visible_count(*asteroid, asteroids, max_x, max_y);
        if visible_count > max_visible_count {
            max_visible_count = visible_count;
            monitoring_station = *asteroid;
        }
    }
    (max_visible_count, monitoring_station)
}

fn modulo(a: f32, n: f32) -> u32 {
    ((a - (a / n).floor() * n) * 100000000f32) as u32
}

fn part2(asteroids: &Vec<Asteroid>, monitoring_station: Asteroid) -> i32 {
    let mut asteroids_angle_distances = Vec::new();
    for asteroid in asteroids {
        if *asteroid != monitoring_station {
            let delta = asteroid - monitoring_station;
            asteroids_angle_distances.push((
                asteroid,
                f32::atan2(delta.re as f32, delta.im as f32) + std::f32::consts::PI,
                i32::abs(delta.re) + i32::abs(delta.im),
            ));
        }
    }
    let mut target_count = 1;
    let mut angle = 2f32 * std::f32::consts::PI;
    let mut last_removed = Asteroid::new(-1, -1);
    while target_count <= 200 {
        let next = asteroids_angle_distances
            .iter()
            .min_by_key(|&(_, asteroid_angle, distance)| {
                (
                    if angle == *asteroid_angle || target_count == 1 {
                        1
                    } else {
                        0
                    },
                    modulo(angle - asteroid_angle, 2f32 * std::f32::consts::PI),
                    distance,
                )
            })
            .unwrap();
        if let Some(position) = asteroids_angle_distances
            .iter()
            .position(|&entry| entry == *next)
        {
            let (asteroid, asteroid_angle, _) = asteroids_angle_distances.remove(position);
            last_removed = *asteroid;
            angle = asteroid_angle;
            target_count += 1;
        }
    }
    i32::abs(last_removed.re) * 100 + i32::abs(last_removed.im)
}

fn solve(asteroids: &Vec<Asteroid>) -> (u32, i32) {
    let (max_visible_count, monitoring_station) = part1(asteroids);
    (max_visible_count, part2(asteroids, monitoring_station))
}

fn get_input(file_path: &String) -> Vec<Asteroid> {
    let mut asteroids = Vec::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                asteroids.push(Asteroid::new(x as i32, y as i32));
            }
        }
    }
    asteroids
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
