require 'minitest/autorun'
require 'image'

class TestImage < Minitest::Test
    def test_part1()
        assert_equal 1, image_check_corruption('123456789012', 3, 2)
    end

    def test_part2()
        assert_equal [[PIXEL_BLACK, PIXEL_WHITE], [PIXEL_WHITE, PIXEL_BLACK]], image_get_output('0222112222120000', 2, 2)
    end
end