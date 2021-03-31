use core::fmt::Debug;
use std::collections::HashMap;

type Universe = HashMap<Coordinate, bool>;

trait UniverseFuncs {
    fn is_active(&self, coordinate: &Coordinate) -> bool;
    fn dimension_count(&self) -> usize;
}

impl UniverseFuncs for Universe {
    fn is_active(&self, coordinate: &Coordinate) -> bool {
        match self.get(coordinate) {
            Some(true) => true,
            _ => false,
        }
    }

    fn dimension_count(&self) -> usize {
        self.keys().next().unwrap().count()
    }
}

struct CoordinateIterator {
    lower: Coordinate,
    upper: Coordinate,
    current: Coordinate,
}

impl CoordinateIterator {
    fn new(lower: &Coordinate, upper: &Coordinate) -> CoordinateIterator {
        CoordinateIterator {
            lower: lower.clone(),
            upper: upper.clone(),
            current: lower.add_last(-1),
        }
    }

    fn from_universe(universe: &Universe) -> CoordinateIterator {
        CoordinateIterator::new(
            &Coordinate::new(
                &(0..universe.dimension_count())
                    .into_iter()
                    .map(|index| universe.keys().map(|c| c.nth(index)).min().unwrap() - 1)
                    .collect(),
            ),
            &Coordinate::new(
                &(0..universe.dimension_count())
                    .into_iter()
                    .map(|index| universe.keys().map(|c| c.nth(index)).max().unwrap() + 1)
                    .collect(),
            ),
        )
    }

    fn _get_limits(universe: &Universe) -> (Coordinate, Coordinate) {
        (
            Coordinate::new(
                &(0..universe.dimension_count())
                    .into_iter()
                    .map(|index| universe.keys().map(|c| c.nth(index)).min().unwrap())
                    .collect(),
            ),
            Coordinate::new(
                &(0..universe.dimension_count())
                    .into_iter()
                    .map(|index| universe.keys().map(|c| c.nth(index)).max().unwrap())
                    .collect(),
            ),
        )
    }

    fn next_coordinate_value(
        current: &Coordinate,
        lower_limits: &Coordinate,
        upper_limits: &Coordinate,
    ) -> Coordinate {
        let mut result = current.to_vec();
        for index in (0..current.count()).rev() {
            if current.nth(index) < upper_limits.nth(index) {
                result[index] += 1;
                for overflow in index + 1..current.count() {
                    result[overflow] = lower_limits.nth(overflow);
                }
                break;
            }
        }
        Coordinate::new(&result)
    }
}

impl Iterator for CoordinateIterator {
    type Item = Coordinate;

    fn next(&mut self) -> Option<<Self as std::iter::Iterator>::Item> {
        if self.current == self.upper {
            None
        } else {
            let mut result = self.current.to_vec();
            for index in (0..self.current.count()).rev() {
                if self.current.nth(index) < self.upper.nth(index) {
                    result[index] += 1;
                    for overflow in index + 1..self.current.count() {
                        result[overflow] = self.lower.nth(overflow);
                    }
                    break;
                }
            }
            self.current =
                CoordinateIterator::next_coordinate_value(&self.current, &self.lower, &self.upper);
            Some(Coordinate::new(&result))
        }
    }
}

impl Debug for Coordinate {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> Result<(), std::fmt::Error> {
        f.debug_list().entries(&self.coordinates).finish()
    }
}

struct Coordinate {
    coordinates: Vec<i32>,
}

impl std::cmp::Eq for Coordinate {}

impl std::cmp::PartialEq for Coordinate {
    fn eq(&self, other: &Self) -> bool {
        self.coordinates == other.coordinates
    }
}

impl std::hash::Hash for Coordinate {
    fn hash<H>(&self, state: &mut H)
    where
        H: std::hash::Hasher,
    {
        self.coordinates.hash(state);
    }
}

impl Coordinate {
    fn new(coordinates: &Vec<i32>) -> Coordinate {
        Coordinate {
            coordinates: coordinates.into_iter().map(|c| *c).collect(),
        }
    }

    fn nth(&self, index: usize) -> i32 {
        self.coordinates[index]
    }

    fn count(&self) -> usize {
        self.coordinates.len()
    }

    fn add(&self, value: i32) -> Coordinate {
        Coordinate::new(
            &self
                .coordinates
                .iter()
                .map(|c| c + value)
                .collect::<Vec<i32>>(),
        )
    }

    fn add_last(&self, value: i32) -> Coordinate {
        let mut coordinates = self.to_vec();
        coordinates[self.count() - 1] += value;
        Coordinate::new(&coordinates)
    }

    fn add_dimension(&self) -> Coordinate {
        let mut coordinates = self.to_vec();
        coordinates.insert(0, 0);
        Coordinate::new(&coordinates)
    }

    fn to_vec(&self) -> Vec<i32> {
        self.coordinates.clone()
    }

    fn clone(&self) -> Coordinate {
        Coordinate::new(&self.to_vec())
    }
}

fn _print_universe(universe: &Universe) {
    let dimension_count = universe.dimension_count();
    let (lower_limits, upper_limits) = CoordinateIterator::_get_limits(universe);
    const OUTER_DIMENSIONS: [&str; 2] = ["z", "w"];
    for coordinate in CoordinateIterator::new(&lower_limits, &upper_limits) {
        if coordinate.nth(dimension_count - 1) == lower_limits.nth(dimension_count - 1)
            && coordinate.nth(dimension_count - 2) == lower_limits.nth(dimension_count - 2)
        {
            println!();
            print!(
                "{}",
                (0..dimension_count - 2)
                    .into_iter()
                    .map(|index| format!("{}={}", OUTER_DIMENSIONS[index], coordinate.nth(index)))
                    .collect::<Vec<String>>()
                    .join(",")
            );
        }
        if coordinate.nth(dimension_count - 1) == lower_limits.nth(dimension_count - 1) {
            println!();
        }
        print!(
            "{}",
            if universe.is_active(&coordinate) {
                '#'
            } else {
                '.'
            }
        );
    }
    println!();
}

fn get_active_neighbor_count(universe: &Universe, coordinate: &Coordinate) -> usize {
    CoordinateIterator::new(&coordinate.add(-1), &coordinate.add(1))
        .filter(|neighbor| neighbor != coordinate && universe.is_active(&neighbor))
        .count()
}

fn next_cycle(universe: &Universe) -> Universe {
    let mut new_state = Universe::new();
    for coordinate in CoordinateIterator::from_universe(universe) {
        let active_native_neighbor_count = get_active_neighbor_count(universe, &coordinate);
        new_state.insert(
            coordinate.clone(),
            if let Some(true) = universe.get(&coordinate) {
                active_native_neighbor_count == 2 || active_native_neighbor_count == 3
            } else {
                active_native_neighbor_count == 3
            },
        );
    }
    new_state
}

fn run_cycles(universe: &Universe) -> usize {
    let mut universe: Universe = universe.into_iter().map(|(c, v)| (c.clone(), *v)).collect();
    for _ in 0..6 {
        universe = next_cycle(&universe);
    }
    universe.values().filter(|v| **v).count()
}

fn solve(universe: &Universe) -> (usize, usize) {
    (
        run_cycles(universe),
        run_cycles(
            &universe
                .into_iter()
                .map(|(coordinate, value)| (coordinate.add_dimension(), *value))
                .collect(),
        ),
    )
}

fn get_input(file_path: &String) -> Universe {
    let mut universe = Universe::new();
    for (y, line) in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
        .enumerate()
    {
        for (x, c) in line.chars().enumerate() {
            universe.insert(Coordinate::new(&vec![0, y as i32, x as i32]), c == '#');
        }
    }
    universe
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
