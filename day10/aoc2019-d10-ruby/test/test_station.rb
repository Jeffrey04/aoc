require 'minitest/autorun'
require 'station'

class TestIntcoder < Minitest::Test
  def test_part1
    assert_equal [[3, 4], 8], station_find_best('.#..#
.....
#####
....#
...##'.split("\n"))
    assert_equal [[5,8], 33], station_find_best('......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####'.split("\n"))
    assert_equal [[1,2], 35], station_find_best('#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.'.split("\n"))
    assert_equal [[6,3], 41], station_find_best('.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..'.split("\n"))
    assert_equal [[11,13], 210], station_find_best('.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'.split("\n"))
  end

  def test_part2
    sequence = station_vaporize_asteroids('.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##'.split("\n"))
    assert_equal [8, 1], sequence[0]
    assert_equal [9, 0], sequence[1]
    assert_equal [9, 1], sequence[2]
    assert_equal [10, 0], sequence[3]
    assert_equal [9, 2], sequence[4]
    assert_equal [11, 1], sequence[5]
    assert_equal [12, 1], sequence[6]
    assert_equal [11, 2], sequence[7]
    assert_equal [15, 1], sequence[8]
    assert_equal [12, 2], sequence[9]
    assert_equal [13, 2], sequence[10]
    assert_equal [14, 2], sequence[11]
    assert_equal [15, 2], sequence[12]
    assert_equal [12, 3], sequence[13]
    assert_equal [16, 4], sequence[14]
    assert_equal [15, 4], sequence[15]
    assert_equal [10, 4], sequence[16]
    assert_equal [4, 4], sequence[17]
    assert_equal [2, 4], sequence[18]
    assert_equal [2, 3], sequence[19]
    assert_equal [0, 2], sequence[20]
    assert_equal [1, 2], sequence[21]
    assert_equal [0, 1], sequence[22]
    assert_equal [1, 1], sequence[23]
    assert_equal [5, 2], sequence[24]
    assert_equal [1, 0], sequence[25]
    assert_equal [5, 1], sequence[26]
    assert_equal [6, 1], sequence[27]
    assert_equal [6, 0], sequence[28]
    assert_equal [7, 0], sequence[29]
    assert_equal [8, 0], sequence[30]
    assert_equal [10, 1], sequence[31]
    assert_equal [14, 0], sequence[32]
    assert_equal [16, 1], sequence[33]
    assert_equal [13, 3], sequence[34]
    assert_equal [14, 3], sequence[35]

    sequence = station_vaporize_asteroids('.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##'.split("\n"))
    assert_equal [11,12], sequence[0]
    assert_equal [12,1], sequence[1]
    assert_equal [12,2], sequence[2]
    assert_equal [12,8], sequence[9]
    assert_equal [16,0], sequence[19]
    assert_equal [16,9], sequence[49]
    assert_equal [10,16], sequence[99]
    assert_equal [9,6], sequence[198]
    assert_equal [9,6], sequence[198]
    assert_equal [8,2], sequence[199]
    assert_equal [10,9], sequence[200]
    assert_equal [11,1], sequence[298]
  end
end