require 'station'

def compute_puzzle1()
    station_find_best(File.readlines(ENV['PUZZLE_INPUT'])).last
end

def compute_puzzle2()
    sequence = station_vaporize_asteroids(File.readlines(ENV['PUZZLE_INPUT']))
    sequence[199].first * 100 + sequence[199].last
end

puts("RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}")