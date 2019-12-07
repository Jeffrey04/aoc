def distance_measure(alpha, beta)
    intersection_closest(intersection_find(
        path_trace(path_break(alpha)),
        path_trace(path_break(beta))
    ))
end

def intersection_find(alpha, beta)
    alpha.select{|point_alpha|
        beta.select{|point_beta|
            point_alpha.first == point_beta.first \
                && point_alpha.last == point_beta.last
        }.empty? == false
    }
end

def intersection_closest(intersection)
    intersection[1, intersection.size].reduce(Float::INFINITY) {|current, incoming|
        current < incoming.first + incoming.last \
            ? current
            : incoming.first + incoming.last
    }
end

def move_one(path)
    path.map.with_index{|line, idx|
        result = line

        if idx == 0
            result = [line.first, line.last - 1]
        end

        result
    }
end

def move_down(points)
    points << [points.last.first, points.last.last - 1]
end

def move_left(points)
    points << [points.last.first - 1, points.last.last]
end

def move_right(points)
    points << [points.last.first + 1, points.last.last]
end

def move_up(points)
    points << [points.last.first, points.last.last + 1]
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
    elsif path.first.last == 0
        result = path_trace(path[1, path.size], points)
    elsif path.first.first == 'R'
        result = path_trace(move_one(path), move_right(points))
    elsif path.first.first == 'L'
        result = path_trace(move_one(path), move_left(points))
    elsif path.first.first == 'U'
        result = path_trace(move_one(path), move_up(points))
    elsif path.first.first == 'D'
        result = path_trace(move_one(path), move_down(points))
    end

    result
end