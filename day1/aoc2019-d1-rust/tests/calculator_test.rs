extern crate aoc2019_d1_rust;

use aoc2019_d1_rust::calculator;

#[test]
fn test_fuel_calculator() {
    assert_eq!(2, calculator::fuel_calculate(12));
    assert_eq!(2, calculator::fuel_calculate(14));
    assert_eq!(654, calculator::fuel_calculate(1969));
    assert_eq!(33583, calculator::fuel_calculate(100756));
}