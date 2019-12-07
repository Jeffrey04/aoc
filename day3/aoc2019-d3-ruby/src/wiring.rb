def distance_measure(alpha, beta)
    intersection_closest(
        path_trace(path_break(alpha)) & path_trace(path_break(beta))
    )
end

def intersection_closest(intersection)
    intersection[1, intersection.size].reduce(Float::INFINITY) {|current, incoming|
        current < incoming.first + incoming.last \
            ? current
            : incoming.first + incoming.last
    }
end

def move_down(points, steps)
    steps == 0 \
        ? points
        : move_down(points << [points.last.first, points.last.last - 1], steps - 1)
end

def move_left(points, steps)
    steps == 0 \
        ? points
        : move_left(points << [points.last.first - 1, points.last.last], steps - 1)
end

def move_right(points, steps)
    steps == 0 \
        ? points
        : move_right(points << [points.last.first + 1, points.last.last], steps - 1)
end

def move_up(points, steps)
    steps == 0 \
        ? points
        : move_up(points << [points.last.first, points.last.last + 1], steps - 1)
end

def path_break(path)
    path.split(',')
        .map{|line|
            [line[0], line[1,line.size].to_i]
        }
end

def path_trace(path, points=[[0, 0]])
    result = false

    if path.empty?
        result = points
    elsif path.first.first == 'R'
        result = path_trace(path[1, path.size], move_right(points, path.first.last))
    elsif path.first.first == 'L'
        result = path_trace(path[1, path.size], move_left(points, path.first.last))
    elsif path.first.first == 'U'
        result = path_trace(path[1, path.size], move_up(points, path.first.last))
    elsif path.first.first == 'D'
        result = path_trace(path[1, path.size], move_down(points, path.first.last))
    end

    result
end