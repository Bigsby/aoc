use num::complex::Complex;
use regex::Regex;
use std::collections::{HashMap, HashSet, VecDeque};

type Lattice = Complex<i32>;
type Grid = HashSet<Lattice>;
type Rule = (Grid, Grid);
type Rules = HashMap<i32, Vec<Rule>>;
static START: &'static str = ".#./..#/###";

fn _print_grid(grid: &Grid) {
    let max_x = grid.iter().map(|p| p.re).max().unwrap();
    let max_y = grid.iter().map(|p| p.im).max().unwrap();
    for y in 0..max_y + 1 {
        for x in 0..max_x + 1 {
            print!(
                "{}",
                if grid.contains(&Lattice::new(x, y)) {
                    '#'
                } else {
                    '.'
                }
            );
        }
        println!();
    }
    println!();
}

fn parse_grid(text: &str) -> (i32, Grid) {
    let mut grid = Grid::new();
    let split = text.split('/').collect::<Vec<&str>>();
    for (y, line) in split.iter().enumerate() {
        for (x, c) in line.chars().enumerate() {
            if c == '#' {
                grid.insert(Lattice::new(x as i32, y as i32));
            }
        }
    }
    return (split[0].len() as i32, grid);
}

fn mirror_horizontal(grid: &Grid, size: i32) -> Grid {
    grid.into_iter()
        .map(|position| Lattice::new(size - 1 - position.re, position.im))
        .collect()
}

fn rotate_clockwise(grid: &Grid, size: i32) -> Grid {
    grid.into_iter()
        .map(|position| Lattice::new(size - 1 - position.im, position.re))
        .collect()
}

fn generate_permutations(grid: &Grid, size: i32) -> Vec<Grid> {
    let mut permutations = Vec::new();
    let mut grid = grid.clone();
    for _ in 0..4 {
        permutations.push(grid.clone());
        permutations.push(mirror_horizontal(&grid, size));
        grid = rotate_clockwise(&grid, size);
    }
    permutations
}

fn enhance_grid(grid: &Grid, size: i32, rules: &Vec<Rule>) -> Grid {
    for permutation in generate_permutations(grid, size) {
        for (match_grid, result) in rules {
            if match_grid == &permutation {
                return result.clone();
            }
        }
    }
    panic!("Rule not found");
}

fn split_grid(grid: &Grid, count: i32, size: i32) -> Vec<(i32, i32, Grid)> {
    let mut grids = Vec::new();
    for y_index in 0..count {
        for x_index in 0..count {
            let x_offset = x_index * size;
            let y_offset = y_index * size;
            let inner_grid: Grid = grid
                .iter()
                .filter(|p| {
                    p.re >= x_offset
                        && p.re < x_offset + size
                        && p.im >= y_offset
                        && p.im < y_offset + size
                })
                .map(|p| Lattice::new(p.re - x_index * size, p.im - y_index * size))
                .collect();
            grids.push((x_index, y_index, inner_grid));
        }
    }
    grids
}

fn iterate(grid: &Grid, size: i32, rules: &Rules) -> (i32, Grid) {
    let mut enhanced_grid = Grid::new();
    let mut rule_size = 0;
    if size % 2 == 0 {
        rule_size = 2;
    } else if size % 3 == 0 {
        rule_size = 3;
    }
    let rule_set = rules.get(&rule_size).unwrap();
    let divider = size / rule_size;
    for (x_index, y_index, inner_grid) in split_grid(grid, divider, rule_size) {
        for position in enhance_grid(&inner_grid, rule_size, rule_set) {
            enhanced_grid.insert(Lattice::new(
                position.re + x_index * (rule_size + 1),
                position.im + y_index * (rule_size + 1),
            ));
        }
    }
    (size + divider, enhanced_grid)
}

fn run_iterations(grid: &Grid, size: i32, rules: &Rules, iterations: i32) -> (i32, Grid) {
    let mut size = size;
    let mut grid = grid.clone();
    for _ in 0..iterations {
        let (new_size, new_grid) = iterate(&grid, size, rules);
        size = new_size;
        grid = new_grid;
    }
    (size, grid)
}

fn run_next_3_iterations(grid: &Grid, rules: &Rules) -> Vec<Grid> {
    let (_, grid) = run_iterations(grid, 3, rules, 3);
    split_grid(&grid, 3, 3)
        .into_iter()
        .map(|(_, _, inner_grid)| inner_grid)
        .collect()
}

fn get_grid_id(grid: &Grid) -> i32 {
    grid.into_iter()
        .fold(0, |acc, p| acc + (1 << p.re << 3 * p.im))
}

fn part2(rules: &Rules, grid: &Grid) -> usize {
    let mut total = 0;
    let mut calculated = HashMap::new();
    let mut queue = VecDeque::new();
    queue.push_front((grid.clone(), 0));
    while let Some((grid, iterations)) = queue.pop_front() {
        if iterations == 18 {
            total += grid.len();
        } else {
            let grid_id = get_grid_id(&grid);
            if !calculated.contains_key(&grid_id) {
                calculated.insert(grid_id, run_next_3_iterations(&grid, rules));
            }
            for inner_grid in calculated.get(&grid_id).unwrap() {
                queue.push_front((inner_grid.clone(), iterations + 3));
            }
        }
    }
    total
}

fn solve(rules: &Rules) -> (usize, usize) {
    let (size, grid) = parse_grid(START);
    (
        run_iterations(&grid, size, rules, 5).1.len(),
        part2(rules, &grid),
    )
}

fn parse_line(line: &str) -> (i32, Rule) {
    let line_regex = Regex::new(r"^(?P<rule>[./#]+) => (?P<result>[./#]+)$").unwrap();
    if let Some(cap) = line_regex.captures(line) {
        let (rule_size, rule_grid) = parse_grid(cap.name("rule").unwrap().as_str());
        let (_, result_grid) = parse_grid(cap.name("result").unwrap().as_str());
        return (rule_size, (rule_grid, result_grid));
    }
    panic!("Bad format: {}", line);
}

fn get_input(file_path: &String) -> Rules {
    let mut rules = Rules::new();
    let mut rules2 = Vec::new();
    let mut rules3 = Vec::new();
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        let (size, rule) = parse_line(line);
        match size {
            2 => rules2.push(rule),
            3 => rules3.push(rule),
            _ => {
                panic!("Unacceptable size '{}'", size);
            }
        }
    }
    rules.insert(2, rules2);
    rules.insert(3, rules3);
    rules
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
