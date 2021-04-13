use num::complex::Complex;
use regex::Regex;
use std::collections::HashMap;

type Lattice = Complex<i32>;
type Tile = Vec<Lattice>;

struct TileMatcher {
    tests: HashMap<Lattice, (Lattice, Lattice, Lattice)>,
    sides: Vec<Lattice>,
}

impl TileMatcher {
    fn new() -> TileMatcher {
        TileMatcher {
            sides: vec![
                Lattice::new(0, -1),
                Lattice::new(1, 0),
                Lattice::new(0, 1),
                Lattice::new(-1, 0),
            ],
            tests: vec![
                (
                    Lattice::new(0, -1),
                    (Lattice::new(0, 0), Lattice::new(0, 1), Lattice::new(1, 0)),
                ),
                (
                    Lattice::new(1, 0),
                    (Lattice::new(1, 0), Lattice::new(0, 0), Lattice::new(0, 1)),
                ),
                (
                    Lattice::new(0, 1),
                    (Lattice::new(0, 1), Lattice::new(0, 0), Lattice::new(1, 0)),
                ),
                (
                    Lattice::new(-1, 0),
                    (Lattice::new(0, 0), Lattice::new(1, 0), Lattice::new(0, 1)),
                ),
            ]
            .into_iter()
            .collect(),
        }
    }

    fn test_sides(&self, tile_a: &Tile, tile_b: &Tile, side: Lattice, size: i32) -> bool {
        let (position_a_start, position_b_start, step) = self.tests.get(&side).unwrap();
        let mut position_a = position_a_start * size;
        let mut position_b = position_b_start * size;
        for _ in 0..size + 1 {
            if tile_a.contains(&position_a) ^ tile_b.contains(&position_b) {
                return false;
            }
            position_a += step;
            position_b += step;
        }
        true
    }

    fn do_permutations_match(
        &self,
        permutation_a: &Tile,
        permutation_b: &Tile,
        size: i32,
        sides: &Vec<Lattice>,
    ) -> Option<Lattice> {
        for side in sides {
            if self.test_sides(permutation_a, permutation_b, *side, size) {
                return Some(*side);
            }
        }
        None
    }

    fn do_tiles_match(
        &self,
        tile_a: &Tile,
        permutations: &Vec<Tile>,
        size: i32,
        sides: &Vec<Lattice>,
    ) -> Option<(Lattice, Tile)> {
        for permutation in permutations {
            if let Some(side) = self.do_permutations_match(tile_a, permutation, size, sides) {
                return Some((side, permutation.clone()));
            }
        }
        None
    }

    fn get_matching_sides(
        &self,
        tile: &(u32, Tile),
        tiles: &Vec<(u32, Tile)>,
        permutations: &HashMap<u32, Vec<Tile>>,
        size: i32,
    ) -> Vec<Lattice> {
        let (this_number, this_tile) = tile;
        let mut matched_sides = Vec::new();
        for (other_number, _) in tiles {
            if this_number == other_number {
                continue;
            }
            if let Some((side, _)) = self.do_tiles_match(
                this_tile,
                permutations.get(other_number).unwrap(),
                size,
                &self.sides,
            ) {
                matched_sides.push(side)
            }
        }
        matched_sides
    }
}

fn _print_tile(tile: &Tile) {
    let start_x = tile.iter().map(|p| p.re).min().unwrap();
    let end_x = tile.iter().map(|p| p.re).max().unwrap();
    let start_y = tile.iter().map(|p| p.im).min().unwrap();
    let end_y = tile.iter().map(|p| p.im).max().unwrap();
    for row in start_x..end_x + 1 {
        for column in start_y..end_y + 1 {
            print!(
                "{}",
                if tile.contains(&Lattice::new(column, row)) {
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

fn get_size(tile: &Tile, height: bool) -> i32 {
    if height {
        tile.into_iter().map(|p| p.im).max().unwrap()
    } else {
        tile.into_iter().map(|p| p.re).max().unwrap()
    }
}

fn mirror_horizontal(tile: &Tile, size: i32) -> Tile {
    tile.into_iter()
        .map(|lattice| Lattice::new(size - lattice.re, lattice.im))
        .collect()
}

fn rotate_clockwise(tile: &Tile, size: i32) -> Tile {
    tile.into_iter()
        .map(|lattice| Lattice::new(size - lattice.im, lattice.re))
        .collect()
}

fn generate_permutations(tile: &Tile) -> Vec<Tile> {
    let size = get_size(tile, false);
    let mut tile = tile.clone();
    let mut permutations = Vec::new();
    for _ in 0..4 {
        permutations.push(tile.clone());
        permutations.push(mirror_horizontal(&tile, size));
        tile = rotate_clockwise(&tile, size);
    }
    permutations
}

fn generate_all_tiles_permutations(tiles: &Vec<(u32, Tile)>) -> HashMap<u32, Vec<Tile>> {
    tiles
        .into_iter()
        .map(|(number, tile)| (*number, generate_permutations(tile)))
        .collect()
}

fn get_corners(
    tiles: &Vec<(u32, Tile)>,
    size: i32,
    permutations: &HashMap<u32, Vec<Tile>>,
    matcher: &TileMatcher,
) -> Vec<(u32, Vec<Lattice>)> {
    tiles
        .into_iter()
        .map(|tile| {
            (
                tile.0,
                matcher.get_matching_sides(tile, tiles, permutations, size),
            )
        })
        .filter(|(_, matched_sides)| matched_sides.len() == 2)
        .collect()
}

fn build_puzzle(
    tiles: &Vec<(u32, Tile)>,
    tile_size: i32,
    corners: &Vec<(u32, Vec<Lattice>)>,
    permutations: &HashMap<u32, Vec<Tile>>,
    matcher: &TileMatcher,
) -> HashMap<Lattice, Tile> {
    let (first_corner_number, first_sides) = &corners[0];
    let side_one = first_sides[0];
    let side_two = first_sides[1];
    let puzzle_width = (tiles.len() as f32).sqrt() as usize;
    let mut puzzle_lattice = Lattice::new(
        (puzzle_width - 1) as i32
            * (if side_one == Lattice::new(-1, 0) || side_two == Lattice::new(-1, 0) {
                1
            } else {
                0
            }),
        (puzzle_width - 1) as i32
            * (if side_one == Lattice::new(0, -1) || side_two == Lattice::new(0, -1) {
                1
            } else {
                0
            }),
    );
    let mut last_tile = permutations.get(first_corner_number).unwrap()[0].clone();
    let mut puzzle = HashMap::new();
    let mut current_number = first_corner_number;
    puzzle.insert(puzzle_lattice, last_tile.clone());
    let mut direction = side_one;
    while puzzle.len() != tiles.len() {
        puzzle_lattice += direction;
        for (tile_number, permutations) in permutations
            .into_iter()
            .filter(|(number, _)| *number != current_number)
        {
            if let Some((_, matched_permutation)) =
                matcher.do_tiles_match(&last_tile, &permutations, tile_size, &vec![direction])
            {
                puzzle.insert(
                    puzzle_lattice,
                    matched_permutation.iter().map(|p| *p).collect(),
                );
                current_number = tile_number;
                last_tile = matched_permutation.iter().map(|p| *p).collect();
                if direction == side_two {
                    direction = (if (puzzle.len() / puzzle_width) % 2 != 0 {
                        -1
                    } else {
                        1
                    }) * side_one;
                } else if puzzle.len() % puzzle_width == 0 {
                    direction = side_two;
                }
                break;
            }
        }
    }
    puzzle
}

fn remove_borders_and_join(puzzle: &HashMap<Lattice, Tile>, tile_size: i32) -> Tile {
    let offset_factor = tile_size - 1;
    let mut reduced = Tile::new();
    for (puzzle_lattice, tile) in puzzle {
        for lattice in tile {
            if lattice.re > 0 && lattice.re < tile_size && lattice.im > 0 && lattice.im < tile_size
            {
                reduced.push(Lattice::new(
                    puzzle_lattice.re * offset_factor + lattice.re - 1,
                    puzzle_lattice.im * offset_factor + lattice.im - 1,
                ));
            }
        }
    }
    reduced
}

static SEA_MONSTER: &'static [&'static str] = &[
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
];

fn get_sea_monster() -> Tile {
    let mut sea_monster = Tile::new();
    for (row_index, row) in SEA_MONSTER.iter().enumerate() {
        for (column_index, c) in row.chars().enumerate() {
            if c == '#' {
                sea_monster.push(Lattice::new(column_index as i32, row_index as i32));
            }
        }
    }
    sea_monster
}

fn is_monster_in_location(location: Lattice, puzzle: &Tile, sea_monster: &Tile) -> bool {
    for monster_lattice in sea_monster {
        if !puzzle.contains(&(location + monster_lattice)) {
            return false;
        }
    }
    true
}

fn get_sea_monster_count(puzzle: &Tile, sea_monster: &Tile) -> usize {
    let sea_monster_width = get_size(sea_monster, false) + 1;
    let sea_monster_height = get_size(sea_monster, true) + 1;
    let puzzle_size = get_size(puzzle, false) + 1;
    for permutation in generate_permutations(puzzle) {
        let mut count = 0;
        for puzzle_x in 0..puzzle_size - sea_monster_width {
            for puzzle_y in 0..puzzle_size - sea_monster_height {
                if is_monster_in_location(
                    Lattice::new(puzzle_x, puzzle_y),
                    &permutation,
                    sea_monster,
                ) {
                    count += 1;
                }
            }
        }
        if count > 0 {
            return count;
        }
    }
    0
}

fn part2(
    tiles: &Vec<(u32, Tile)>,
    tile_size: i32,
    tile_permutations: &HashMap<u32, Vec<Tile>>,
    corners: &Vec<(u32, Vec<Lattice>)>,
    matcher: &TileMatcher,
) -> usize {
    let puzzle = build_puzzle(tiles, tile_size, corners, tile_permutations, matcher);
    let reduced = remove_borders_and_join(&puzzle, tile_size);
    let sea_monster = get_sea_monster();
    let location_count = get_sea_monster_count(&reduced, &sea_monster);
    reduced.len() - sea_monster.len() * location_count
}

fn solve(tiles: &Vec<(u32, Tile)>) -> (u64, usize) {
    let permutations = generate_all_tiles_permutations(tiles);
    let size = get_size(&tiles[0].1, false);
    let matcher = TileMatcher::new();
    let corners = get_corners(tiles, size, &permutations, &matcher);

    (
        corners
            .iter()
            .fold(1, |acc, (number, _)| acc * *number as u64),
        part2(tiles, size, &permutations, &corners, &matcher),
    )
}

fn get_input(file_path: &String) -> Vec<(u32, Tile)> {
    let number_line_regex = Regex::new(r"^Tile\s(?P<number>\d+):$").unwrap();
    let right = Lattice::new(1, 0);
    let mut tiles = Vec::new();
    let mut tile_number = 0;
    let mut tile = Tile::new();
    let mut lattice = Lattice::new(0, 0);
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        if let Some(cap) = number_line_regex.captures(line) {
            tile_number = cap.name("number").unwrap().as_str().parse().unwrap();
            tile = Tile::new();
            lattice = Lattice::new(0, 0);
        } else if line.is_empty() {
            tiles.push((tile_number, tile.clone()));
        } else {
            for c in line.trim().chars() {
                if c == '#' {
                    tile.push(lattice);
                }
                lattice += right;
            }
            lattice = Lattice::new(0, lattice.im + 1);
        }
    }
    tiles
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
