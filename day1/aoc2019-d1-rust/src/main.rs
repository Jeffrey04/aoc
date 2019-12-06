use aoc2019_d1_rust::calculator;

use std::{
    fs::File,
    path::Path,
    env,
    io::{self, BufRead, BufReader}
};

fn lines_from_file(filename: impl AsRef<Path>) -> io::Result<Vec<String>> {
    BufReader::new(File::open(filename)?).lines().collect()
}

fn compute_puzzle1() -> i32 {
    lines_from_file(env::var("PUZZLE_INPUT").unwrap())
        .unwrap()
        .iter()
        .map(|x| calculator::fuel_calculate(x.parse::<i32>().unwrap()))
        .sum()
}


fn main() {
    println!("RUST:\t{}", compute_puzzle1());
}
