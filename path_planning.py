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
            return (int((point1[0] + point2[0]) / 2), int((point1[1] + point2[1]) / 2))

        if len(left_lane_boundary) == 0 or len(right_lane_boundary) == 0:
            return np.array([])  # Return empty array if any boundary is empty

        path = []
        last_right_index = 0

        for i, left_point in enumerate(left_lane_boundary):
            # Search for corresponding right point starting from last found right index
            for offset, right_point in enumerate(right_lane_boundary[last_right_index:], start=last_right_index):
                if 17 < distance(left_point, right_point) < 27:
                    path.append(midpoint(left_point, right_point))
                    last_right_index = offset  # Update last_right_index to current
                    break  # Move to the next left point after a match is found

        return np.array(path)  # Convert list to numpy array for consistency with input types
