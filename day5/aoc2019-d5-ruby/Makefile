.PHONY: run test

run:
	@PUZZLE_MIN=246540 PUZZLE_MAX=787419 bundle exec ruby -I bin:src src/main.rb

test:
	@bundle exec ruby -I test:src test/test_intcoder.rb