def distance_measure_manhattan(alpha, beta)
    intersection_closest_manhattan(
        path_trace(path_break(alpha)) & path_trace(path_break(beta))
    )
end

def distance_measure_path(alpha, beta)
    alpha_points = path_trace(path_break(alpha))
    beta_points = path_trace(path_break(beta))
    intersection_closest_path(
        alpha_points & beta_points,
        alpha_points,
        beta_points
    )
end

def intersection_closest_manhattan(intersection)
    intersection[1, intersection.size].reduce(Float::INFINITY) {|current, incoming|
        current < incoming.first.abs + incoming.last.abs \
            ? current
            : incoming.first.abs + incoming.last.abs
    }
end

def intersection_closest_path(intersection, alpha_points, beta_points)
    intersection[1, intersection.size].reduce(Float::INFINITY) {|current, incoming|
        incoming_distance = alpha_points.index(incoming) + beta_points.index(incoming)

        current < incoming_distance \
            ? current
            : incoming_distance
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