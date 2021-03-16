use itertools::Itertools;
use regex::Regex;

type Triplet = (i64, i64, i64);

pub struct Moon {
    position: Triplet,
    velocity: Triplet,
}

impl Moon {
    pub fn new(x: i64, y: i64, z: i64) -> Moon {
        Moon {
            position: (x, y, z),
            velocity: (0, 0, 0),
        }
    }
    pub fn update_velocity(&mut self, other_position: Triplet) {
        self.velocity = Moon::sum(
            self.velocity,
            Moon::get_coordinate_delta(self.position, other_position),
        );
    }

    pub fn update_position(&mut self) {
        self.position = Moon::sum(self.position, self.velocity);
    }

    pub fn get_total_energy(&self) -> i64 {
        Moon::sum_abs(self.position) * Moon::sum_abs(self.velocity)
    }

    pub fn clone(&self) -> Moon {
        Moon {
            position: (self.position.0, self.position.1, self.position.2),
            velocity: (self.velocity.0, self.velocity.1, self.velocity.2),
        }
    }

    fn get_delta(this_value: i64, other_value: i64) -> i64 {
        if this_value < other_value {
            1
        } else if this_value > other_value {
            -1
        } else {
            0
        }
    }

    fn get_coordinate_delta(one: Triplet, two: Triplet) -> Triplet {
        (
            Moon::get_delta(one.0, two.0),
            Moon::get_delta(one.1, two.1),
            Moon::get_delta(one.2, two.2),
        )
    }

    fn sum(one: Triplet, two: Triplet) -> Triplet {
        (one.0 + two.0, one.1 + two.1, one.2 + two.2)
    }

    fn sum_abs(coordinate: Triplet) -> i64 {
        i64::abs(coordinate.0) + i64::abs(coordinate.1) + i64::abs(coordinate.2)
    }
}

fn run_step(moons: &mut Vec<Moon>) {
    for pair in (0..moons.len()).into_iter().combinations(2) {
        let first_position = moons[pair[0]].position;
        let second_position = moons[pair[1]].position;
        moons[pair[0]].update_velocity(second_position);
        moons[pair[1]].update_velocity(first_position);
    }
    for moon in moons {
        moon.update_position()
    }
}

fn part1(moons: &Vec<Moon>) -> i64 {
    let mut moons: Vec<Moon> = moons.into_iter().map(|moon| moon.clone()).collect();
    for _ in 0..1000 {
        run_step(&mut moons)
    }
    moons
        .into_iter()
        .fold(0, |acc, moon| acc + moon.get_total_energy())
}

fn gcd(a: i64, b: i64) -> i64 {
    let mut a = a;
    let mut b = b;
    while a != 0 && b != 0 {
        if a > b {
            a %= b;
        } else {
            b %= a;
        }
    }
    a | b
}

type CoordinateState = (Vec<i64>, Vec<i64>);

fn coordinate_getter(triplet: &Triplet, coordinate: usize) -> i64 {
    match coordinate {
        0 => triplet.0,
        1 => triplet.1,
        2 => triplet.2,
        _ => panic!("Invalid coordinate '{}'", coordinate),
    }
}

fn build_state_for_coordinate(moons: &Vec<Moon>, coordinate: usize) -> CoordinateState {
    (
        moons
            .iter()
            .map(|moon| coordinate_getter(&moon.position, coordinate))
            .collect(),
        moons
            .iter()
            .map(|moon| coordinate_getter(&moon.velocity, coordinate))
            .collect(),
    )
}

fn part2(moons: &Vec<Moon>) -> i64 {
    let mut moons: Vec<Moon> = moons.into_iter().map(|moon| moon.clone()).collect();
    let initial_states: Vec<CoordinateState> = (0..3)
        .into_iter()
        .map(|coordinate| build_state_for_coordinate(&moons, coordinate))
        .collect();
    let mut cycles = vec![0i64; 3];
    let mut step = 0i64;
    while cycles.iter().any(|cycle| *cycle == 0) {
        step += 1;
        run_step(&mut moons);
        for coordinate in 0..3 {
            if cycles[coordinate] == 0 {
                let current_state = build_state_for_coordinate(&moons, coordinate);
                if current_state == initial_states[coordinate] {
                    cycles[coordinate] = step;
                }
            }
        }
    }
    cycles
        .into_iter()
        .fold(1i64, |acc, cycle| acc * cycle / gcd(acc, cycle))
}

fn solve(moons: &Vec<Moon>) -> (i64, i64) {
    (part1(moons), part2(moons))
}

fn get_input(file_path: &String) -> Vec<Moon> {
    let line_regex = Regex::new(r"^<x=(?P<x>-?\d+),\sy=(?P<y>-?\d+),\sz=(?P<z>-?\d+)>$").unwrap();
    std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .map(|line| {
            line_regex
                .captures(line)
                .map(|cap| {
                    Moon::new(
                        cap.name("x").unwrap().as_str().parse().unwrap(),
                        cap.name("y").unwrap().as_str().parse().unwrap(),
                        cap.name("z").unwrap().as_str().parse().unwrap(),
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
