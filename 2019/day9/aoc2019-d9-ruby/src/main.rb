require 'intcoder'

def compute_puzzle1()
    intcode_compute(File.readlines(ENV['PUZZLE_INPUT']).join(''), 1).last.last
end

def compute_puzzle2()
    intcode_compute(File.readlines(ENV['PUZZLE_INPUT']).join(''), 2).last.last
end

puts("RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}")