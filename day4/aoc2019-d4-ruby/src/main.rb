require 'password'

def compute_puzzle1()
    password_get_candidates(
        method(:password_is_good),
        ENV['PUZZLE_MIN'],
        ENV['PUZZLE_MAX']).size
end

def compute_puzzle2()
    password_get_candidates(
        method(:password_is_good_too),
        ENV['PUZZLE_MIN'],
        ENV['PUZZLE_MAX']).size
end

puts "RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}"