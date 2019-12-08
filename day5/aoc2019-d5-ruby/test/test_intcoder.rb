require 'minitest/autorun'
require 'intcoder'

class TestIntcoder < Minitest::Test
  def test_part1
    assert_equal [[1002, 4, 3, 4, 99], 0], intcode_compute('1002,4,3,4,33', '1')
    assert_equal [[1101, 100, -1, 4, 99], 0], intcode_compute('1101,100,-1,4,0', '1')
    assert_equal [[1, 0, 99], 0], intcode_compute('03, 0, 99', '1')
    assert_equal [[1101, 1, -1, 0, 04, 3, 99], 0], intcode_compute('1101, 1, -1, 3, 04, 3, 99', '1')
  end

  def test_part2
  end
end