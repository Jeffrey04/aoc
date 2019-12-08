require 'intcoder'

def compute_puzzle1()
    amplifier_phase_get_best(File.readlines(ENV['PUZZLE_INPUT']).join('')).last
end

def compute_puzzle2()
end

puts("RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}")