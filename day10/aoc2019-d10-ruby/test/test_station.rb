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
end