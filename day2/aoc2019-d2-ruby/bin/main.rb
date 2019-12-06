require 'intcoder'

def compute_puzzle1()
    intcode_compute(
        File.readlines(ENV['PUZZLE_INPUT']).join(''),
        12,
        2)
end

puts "Answer for puzzle 1 is #{compute_puzzle1[0]}"