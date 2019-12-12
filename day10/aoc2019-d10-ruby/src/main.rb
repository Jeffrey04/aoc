require 'station'

def compute_puzzle1()
    station_find_best(File.readlines(ENV['PUZZLE_INPUT'])).last
end

def compute_puzzle2()
end

puts("RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}")