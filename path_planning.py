from __future__ import annotations
import math
import numpy as np

class PathPlanning:
    def __init__(self):
        # Constructor can be used for initialization if needed
        pass

    def plan(self, left_lane_boundary: np.ndarray, right_lane_boundary: np.ndarray) -> np.ndarray:

        def distance(point1: tuple, point2: tuple) -> float:
            return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

        def midpoint(point1: tuple, point2: tuple) -> tuple:
            offset = 2
            x_dif = int(point2[0] - point1[0])
            y_dif = int(point2[1] - point1[1])
            x_mid = int(x_dif / 2)
            y_mid = int(y_dif / 2)


            return (point1[0] + x_mid, point1[1] + y_mid)

        if len(left_lane_boundary) == 0 or len(right_lane_boundary) == 0:
            return np.array([])

        path = []
        last_right_index = 0

        for i, left_point in enumerate(left_lane_boundary):
            # Search for corresponding right point starting from last found right index
            for offset, right_point in enumerate(right_lane_boundary[last_right_index:], start=last_right_index):
                if 17 < distance(left_point, right_point) < 26:
                    path.append(midpoint(left_point, right_point))
                    last_right_index = offset  # Update last_right_index to current
                    break  # Move to the next left point after a match is found

        return np.array(path)  # Convert list to numpy array for consistency with input types
