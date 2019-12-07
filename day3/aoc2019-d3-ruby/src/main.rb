require 'wiring'

def compute_puzzle1()
    distance_measure_manhattan(*File.readlines(ENV['PUZZLE_INPUT']))
end

def compute_puzzle2()
    distance_measure_path(*File.readlines(ENV['PUZZLE_INPUT']))
end

puts "RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}"