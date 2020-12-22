# run this https://www.sitepoint.com/minitest-shoulda/
require 'minitest/autorun'
require 'calculator'

class TestCalculator < Minitest::Test
  def test_part1
    assert_equal 2, fuel_calculator(12)
    assert_equal 2, fuel_calculator(14)
    assert_equal 654, fuel_calculator(1969)
    assert_equal 33583, fuel_calculator(100756)
  end

  def test_part2
    assert_equal 2, fuel_fuel_calculator(14)
    assert_equal 966, fuel_fuel_calculator(1969)
    assert_equal 50346, fuel_fuel_calculator(100756)
  end
end