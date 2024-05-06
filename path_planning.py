from __future__ import annotations
import math
import numpy as np

class PathPlanning:
    def __init__(self):
        pass

    def plan(self, left_lane_boundary: np.ndarray, right_lane_boundary: np.ndarray) -> (np.ndarray, np.ndarray):

        def distance(point1: tuple, point2: tuple) -> float:
            return math.sqrt((point1[0] - point2[0]) ** 2 + ((point1[1] - point2[1]) * 0.6) ** 2)


        def midpoint(point1: tuple, point2: tuple) -> tuple:
            x_dif = int(point2[0] - point1[0])
            y_dif = int(point2[1] - point1[1])
            x_mid = int(x_dif / 2)
            y_mid = int(y_dif / 2)


            return (point1[0] + x_mid, point1[1] + y_mid)

        if len(left_lane_boundary) == 0 or len(right_lane_boundary) == 0:
            return np.array([]), np.array([])

        path = []
        last_right_index = 0

        for i, left_point in enumerate(left_lane_boundary):
            for offset, right_point in enumerate(right_lane_boundary[last_right_index:], start=last_right_index):
                if 19.5 < distance(left_point, right_point) < 21:
                    path.append(midpoint(left_point, right_point))
                    last_right_index = offset
                    break

        path.append((48,48))
        return np.array(path), np.array([])
