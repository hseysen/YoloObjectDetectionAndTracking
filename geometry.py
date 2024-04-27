import numpy as np


class Line:
    def __init__(self, start_x, start_y, end_x, end_y):
        self.start = np.array([start_x, start_y])
        self.end = np.array([end_x, end_y])


class Point:
    def __init__(self, x, y):
        self.pt = np.array([x, y])
    
    def update(self, new_x, new_y):
        self.pt = np.array([new_x, new_y])


def point_side(line, point):
    return np.sign(np.cross(line.end - line.start, point.pt - line.start))
