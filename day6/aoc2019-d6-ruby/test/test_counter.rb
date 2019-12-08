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

  def test_part2
    assert_equal 4, orbit_count_hops('COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'.split("\n"),
        'YOU',
        'SAN')
  end
end