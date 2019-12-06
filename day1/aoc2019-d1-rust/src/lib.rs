pub mod calculator {
    pub fn fuel_calculate(mass: i32) -> i32 {
        (mass as f64 / 3.0).floor() as i32 - 2
    }
}