require 'counter'

def compute_puzzle1()
    orbit_count(File.readlines(ENV['PUZZLE_INPUT']))
end

def compute_puzzle2()
end

puts("RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}")