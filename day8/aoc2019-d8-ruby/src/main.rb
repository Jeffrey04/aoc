require 'image'

def compute_puzzle1()
    image_check_corruption(File.readlines(ENV['PUZZLE_INPUT']).join(), 25, 6)
end

def compute_puzzle2()
end

puts "RUBY:\t#{compute_puzzle1}\t#{compute_puzzle2}"