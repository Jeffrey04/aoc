require 'minitest/autorun'
require 'password'

class TestIntcoder < Minitest::Test
  def test_part1
    assert_equal true, password_is_good('111111')
    assert_equal false, password_is_good('223450')
    assert_equal false, password_is_good('123789')
  end
end