def fuel_calculator(mass)
    (mass/3).floor - 2
end

def fuel_fuel_calculator(mass, accumulated=0)
    fuel = fuel_calculator(mass)

    fuel <= 0 ?
        accumulated
        : fuel_fuel_calculator(fuel, accumulated + fuel)
end