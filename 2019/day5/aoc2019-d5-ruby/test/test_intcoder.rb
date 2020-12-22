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
    # check for 8-equality
    assert_equal 0, intcode_compute('3,9,8,9,10,9,4,9,99,-1,8', '7').last
    assert_equal 1, intcode_compute('3,9,8,9,10,9,4,9,99,-1,8', '8').last
    assert_equal 0, intcode_compute('3,9,8,9,10,9,4,9,99,-1,8', '9').last

    # check for less than 8
    assert_equal 1, intcode_compute('3,9,7,9,10,9,4,9,99,-1,8', '7').last
    assert_equal 0, intcode_compute('3,9,7,9,10,9,4,9,99,-1,8', '8').last
    assert_equal 0, intcode_compute('3,9,7,9,10,9,4,9,99,-1,8', '9').last

    # check for 8-equality
    assert_equal 0, intcode_compute('3,3,1108,-1,8,3,4,3,99', '7').last
    assert_equal 1, intcode_compute('3,3,1108,-1,8,3,4,3,99', '8').last
    assert_equal 0, intcode_compute('3,3,1108,-1,8,3,4,3,99', '9').last

    # check for less than 8
    assert_equal 1, intcode_compute('3,3,1107,-1,8,3,4,3,99', '7').last
    assert_equal 0, intcode_compute('3,3,1107,-1,8,3,4,3,99', '8').last
    assert_equal 0, intcode_compute('3,3,1107,-1,8,3,4,3,99', '9').last

    # jump tests
    assert_equal 0, intcode_compute('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '0').last
    assert_equal 1, intcode_compute('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '1').last
    assert_equal 1, intcode_compute('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', '-1').last

    # jump tests
    assert_equal 0, intcode_compute('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '0').last
    assert_equal 1, intcode_compute('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '1').last
    assert_equal 1, intcode_compute('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', '-1').last

    # sample program
    assert_equal 999, intcode_compute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', '7').last
    assert_equal 1000, intcode_compute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', '8').last
    assert_equal 1001, intcode_compute('3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
        1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
        999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99', '9').last
  end
end