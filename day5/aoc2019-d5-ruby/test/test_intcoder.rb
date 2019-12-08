require 'minitest/autorun'
require 'intcoder'

class TestIntcoder < Minitest::Test
  def test_legacy
    assert_equal [[3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50], 0], intcode_compute('1,9,10,3,2,3,11,0,99,30,40,50', 1)
    assert_equal [[2, 3, 0, 6, 99], 0], intcode_compute('2,3,0,3,99', 1)
    assert_equal [[2, 4, 4, 5, 99, 9801], 0], intcode_compute('2,4,4,5,99,0', 1)
    assert_equal [[30, 1, 1, 4, 2, 5, 6, 0, 99], 0], intcode_compute('1,1,1,4,99,5,6,0,99', 1)
  end

  def test_part1
    assert_equal [[1002, 4, 3, 4, 99], 0], intcode_compute('1002,4,3,4,33', '1')
    assert_equal [[1101, 100, -1, 4, 99], 0], intcode_compute('1101,100,-1,4,0', '1')
    assert_equal [[1, 0, 99], 0], intcode_compute('3, 0, 99', '1')
    assert_equal [[1101, 1, -1, 0, 04, 3, 99], 0], intcode_compute('1101, 1, -1, 3, 04, 3, 99', '1')
  end

  def test_part2
  end
end