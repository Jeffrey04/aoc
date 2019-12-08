require 'minitest/autorun'
require 'counter'

class TestCounter < Minitest::Test
  def test_part1
    assert_equal 42, orbit_count('COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'.split("\n"))
  end
end