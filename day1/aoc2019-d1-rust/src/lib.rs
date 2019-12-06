pub mod calculator {
    pub fn fuel_calculate(mass: i32) -> i32 {
        (mass as f64 / 3.0).floor() as i32 - 2
    }

    pub fn fuel_fuel_calculate(mass: i32, accumulated: i32) -> i32 {
        let fuel = fuel_calculate(mass);

        if fuel <= 0 {
            accumulated
        } else {
            fuel_fuel_calculate(fuel, accumulated + fuel)
        }
    }
}