require 'calculator'

def compute_puzzle1()
    File.readlines(ENV['PUZZLE_INPUT'])
        .map{|line|
            fuel_calculator(line.to_i)
        }
        .reduce(0) {|current, incoming|
            current + incoming
        }
end

def compute_puzzle2()
    File.readlines(ENV['PUZZLE_INPUT'])
        .map{|line|
            fuel_fuel_calculator(line.to_i)
        }
        .reduce(0) {|current, incoming|
            current + incoming
        }
end

puts("Answer for puzzle 1 is #{compute_puzzle1}")
puts("Answer for puzzle 2 is #{compute_puzzle2}")