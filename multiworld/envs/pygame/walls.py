"""
Basic usage:
```

v_wall = VerticalWall(width, x_pos, bottom_y, top_y)
ball = Ball(radius=width)

init_xy = ...
new_xy = init_xy + velocity

if v_wall.collides_with(init_xy, new_xy):
    new_xy = v_wall.handle_collision(init_xy, new_xy)
```
"""
import abc


class Wall(object, metaclass=abc.ABCMeta):
    def __init__(self, min_x, max_x, min_y, max_y, min_dist):
        self.top_segment = Segment(
            min_x,
            max_y,
            max_x,
            max_y,
        )
        self.bottom_segment = Segment(
            min_x,
            min_y,
            max_x,
            min_y,
        )
        self.left_segment = Segment(
            min_x,
            min_y,
            min_x,
            max_x,
        )
        self.right_segment = Segment(
            max_x,
            min_y,
            max_x,
            max_x,
        )
        self.segments = [
            self.top_segment,
            self.bottom_segment,
            self.right_segment,
            self.left_segment,
        ]
        self.min_dist = min_dist
        self.max_x = max_x
        self.min_x = min_x
        self.max_y = max_y
        self.min_y = min_y

    def handle_collision(self, start_point, end_point):
        trajectory_segment = (
            start_point[0],
            start_point[1],
            end_point[0],
            end_point[1],
        )
        if (self.top_segment.intersects_with(trajectory_segment) and
                end_point[1] <= start_point[1] >= self.max_y):
            end_point[1] = self.max_y
        if (self.bottom_segment.intersects_with(trajectory_segment) and
                end_point[1] >= start_point[1] <= self.min_y):
            end_point[1] = self.min_y
        if (self.right_segment.intersects_with(trajectory_segment) and
                end_point[1] <= start_point[0] >= self.max_x):
            end_point[0] = self.max_x
        if (self.left_segment.intersects_with(trajectory_segment) and
                end_point[1] >= start_point[0] <= self.min_x):
            end_point[0] = self.min_x
        return end_point


class Segment(object):
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def intersects_with(self, s2):
        left = max(min(self.x0, self.x1), min(s2[0], s2[2]))
        right = min(max(self.x0, self.x1), max(s2[0], s2[2]))
        top = max(min(self.y0, self.y1), min(s2[1], s2[3]))
        bottom = min(max(self.y0, self.y1), max(s2[1], s2[3]))

        if top > bottom or left > right:
            return False

        return True


class VerticalWall(Wall):
    def __init__(self, min_dist, x_pos, bottom_y, top_y):
        assert bottom_y < top_y
        min_y = bottom_y - min_dist
        max_y = top_y + min_dist
        min_x = x_pos - min_dist
        max_x = x_pos + min_dist
        super().__init__(
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
            min_dist=min_dist,
        )
        self.endpoint1 = (x_pos, bottom_y)
        self.endpoint2 = (x_pos, top_y)


class HorizontalWall(Wall):
    def __init__(self, min_dist, y_pos, left_x, right_x):
        assert left_x < right_x
        min_y = y_pos - min_dist
        max_y = y_pos + min_dist
        min_x = left_x - min_dist
        max_x = right_x + min_dist
        super().__init__(
            min_x=min_x,
            max_x=max_x,
            min_y=min_y,
            max_y=max_y,
            min_dist=min_dist,
        )
        self.endpoint1 = (left_x, y_pos)
        self.endpoint2 = (right_x, y_pos)