use itertools::Itertools;
use regex::Regex;
use std::collections::HashMap;

type Part = i32;
type Floor = Vec<Part>;
type Floors = Vec<Floor>;
type Elevator = (Part, Part);
type Move = (usize, usize, Elevator);
type State = (usize, Floors);
const EMPTY_SLOT: Part = 0;

fn is_group_valid(group: &Vec<i32>) -> bool {
    let mut test_group: Vec<i32> = group.clone().into_iter().collect();
    let generators: Vec<i32> = group
        .iter()
        .filter(|part| **part > 0)
        .map(|part| *part)
        .collect();
    for generator in generators {
        if test_group.contains(&(-generator)) {
            test_group.retain(|part| *part != generator && *part != -generator);
        }
    }
    return test_group.is_empty()
        || test_group.iter().any(|part| part > &0) ^ test_group.iter().any(|part| part < &0);
}

fn is_move_valid(current_floor: &Floor, next_floor: &Floor, elevator: &Elevator) -> bool {
    let mut current_test_floor: Vec<i32> = current_floor.clone().into_iter().collect();
    current_test_floor.retain(|part| *part != elevator.0 && *part != elevator.1);
    let mut next_test_floor: Vec<i32> = next_floor.clone().into_iter().collect();
    if elevator.0 != EMPTY_SLOT {
        next_test_floor.push(elevator.0);
    }
    if elevator.1 != EMPTY_SLOT {
        next_test_floor.push(elevator.1)
    }
    is_group_valid(&current_test_floor) && is_group_valid(&next_test_floor)
}

fn make_move(floors: &Floors, move_: &Move) -> State {
    let mut floors: Floors = floors
        .into_iter()
        .clone()
        .map(|floor| floor.clone().into_iter().collect())
        .collect();
    let (current_floor, next_floor, elevator) = move_;
    if elevator.0 != EMPTY_SLOT {
        floors[*current_floor].retain(|part| *part != elevator.0);
        floors[*next_floor].push(elevator.0);
    }
    if elevator.1 != EMPTY_SLOT {
        floors[*current_floor].retain(|part| *part != elevator.1);
        floors[*next_floor].push(elevator.1);
    }
    (*next_floor, floors)
}

fn get_valid_directional_moves(
    state: &State,
    direction: i32,
    possible_moves_groups: &Vec<Elevator>,
) -> Vec<Move> {
    let (current_floor, floors) = state;
    if *current_floor == 0 && direction < 0 {
        return vec![];
    }
    let next_floor = (*current_floor as i32 + direction) as usize;
    if next_floor == floors.len() {
        return vec![];
    }
    if (next_floor == 0 && floors[next_floor].len() == 0)
        || (next_floor == 1 && !(floors[1].len() > 0 || floors[0].len() > 0))
    {
        return vec![];
    }
    let mut valid_moves = Vec::new();
    for move_group in possible_moves_groups {
        if is_move_valid(&floors[*current_floor], &floors[next_floor], move_group) {
            valid_moves.push((*current_floor, next_floor, *move_group));
        }
    }
    valid_moves
}

fn prune_moves(moves: &Vec<Move>) -> Vec<Move> {
    let mut moves: Vec<Move> = moves.clone().into_iter().collect();
    let mut pair_moves: Vec<Move> = moves
        .iter()
        .filter(|move_| (move_.2).0 == -(move_.2).1)
        .map(|move_| *move_)
        .collect();
    if pair_moves.len() > 1 {
        pair_moves.remove(pair_moves.len() - 1);
        moves.retain(|move_| !pair_moves.contains(&move_));
    }
    let upstairs_moves: Vec<Move> = moves
        .iter()
        .filter(|move_| move_.0 < move_.1)
        .map(|move_| *move_)
        .collect();
    let single_up_moves: Vec<Move> = upstairs_moves
        .iter()
        .filter(|move_| (move_.2).0 == EMPTY_SLOT || (move_.2).1 == EMPTY_SLOT)
        .map(|move_| *move_)
        .collect();
    if single_up_moves.len() != upstairs_moves.len() {
        moves.retain(|move_| !single_up_moves.contains(move_));
    }
    let downstairs_moves: Vec<Move> = moves
        .iter()
        .filter(|move_| move_.0 > move_.1)
        .map(|move_| *move_)
        .collect();
    let pair_downstairs_moves: Vec<Move> = downstairs_moves
        .iter()
        .filter(|move_| (move_.2).0 != EMPTY_SLOT && (move_.2).1 != EMPTY_SLOT)
        .map(|move_| *move_)
        .collect();
    if pair_downstairs_moves.len() != downstairs_moves.len() {
        moves.retain(|move_| !pair_downstairs_moves.contains(move_));
    }
    moves
}

fn get_valid_moves(state: &State) -> Vec<Move> {
    let (current_floor, floors) = state;
    let floors: Floors = floors
        .into_iter()
        .clone()
        .map(|floor| floor.clone().into_iter().collect())
        .collect();
    let mut current_floor_list: Floor = floors[*current_floor].clone().into_iter().collect();
    current_floor_list.push(EMPTY_SLOT);

    let possible_move_groups: Vec<Elevator> = current_floor_list
        .into_iter()
        .combinations(2)
        .map(|combination| (combination[0], combination[1]))
        .collect();
    let mut valid_moves = get_valid_directional_moves(state, 1, &possible_move_groups);
    valid_moves.extend(get_valid_directional_moves(
        state,
        -1,
        &possible_move_groups,
    ));
    prune_moves(&valid_moves)
}

fn solve_floors(floors: &Floors, radioisotopes_count: usize) -> u32 {
    let mut queue = Vec::new();
    let floor_count = floors.len();
    queue.push((
        (
            0,
            floors
                .into_iter()
                .clone()
                .map(|floor| floor.clone().into_iter().collect())
                .collect(),
        ),
        0,
    ));
    while !queue.is_empty() {
        let (state, moves_count) = queue.pop().unwrap();
        for move_ in get_valid_moves(&state) {
            let new_state = make_move(&state.1, &move_);
            if new_state.0 == floor_count - 1
                && (new_state.1).clone().iter().last().unwrap().len() == radioisotopes_count * 2
            {
                return moves_count + 1;
            } else {
                queue.push((new_state, moves_count + 1));
            }
        }
    }
    panic!("Solution not found")
}

fn parse_line(line: &str, radioisotopes: &mut HashMap<String, i32>) -> Floor {
    let line_regex =
        Regex::new(r"a (?P<radioisotope>\w+)(?P<part>-compatible microchip| generator)").unwrap();
    let mut floor = Floor::new();
    let mut current_radioisotope = (radioisotopes.len() as i32) + 1;
    for cap in line_regex.captures_iter(line) {
        let radioisotope = cap.name("radioisotope").unwrap().as_str();
        if !radioisotopes.contains_key(radioisotope) {
            radioisotopes.insert(String::from(radioisotope), current_radioisotope);
            current_radioisotope += 1;
        }
        let value = radioisotopes.get(radioisotope).unwrap();
        floor.push(
            if cap.name("part").unwrap().as_str().contains("generator") {
                *value
            } else {
                -value
            },
        );
    }
    floor
}

fn solve(data: &(Floors, HashMap<String, i32>)) -> (u32, u32) {
    let (floors, radioisotopes) = data;
    let mut radioisotopes = radioisotopes.clone();
    let part2_extra = "a elerium generator, a elerium-compatible microchip, a dilithium generator, a dilithium-compatible microchip";
    let part1_result = solve_floors(floors, radioisotopes.len());
    let mut floors: Floors = floors
        .into_iter()
        .clone()
        .map(|floor| floor.clone().into_iter().collect())
        .collect();
    floors[0].extend(parse_line(part2_extra, &mut radioisotopes));
    return (part1_result, solve_floors(&floors, radioisotopes.len()));
}

fn get_input(file_path: &str) -> (Floors, HashMap<String, i32>) {
    let mut floors = Floors::new();
    let mut radioisotopes = HashMap::new();
    for line in std::fs::read_to_string(file_path)
        .expect("Error reading input file!")
        .lines()
    {
        floors.push(parse_line(line, &mut radioisotopes));
    }
    (floors, radioisotopes)
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
