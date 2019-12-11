require 'minitest/autorun'
require 'image'

class TestImage < Minitest::Test
    def test_part1()
        assert_equal 1, image_check_corruption('123456789012', 3, 2)
    end
end