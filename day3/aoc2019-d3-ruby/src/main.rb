require 'wiring'

def compute_puzzle1()
    distance_measure(*File.readlines(ENV['PUZZLE_INPUT']))
end

puts "RUBY: #{compute_puzzle1}"