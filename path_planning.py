from __future__ import annotations
import math
import numpy as np

class PathPlanning:
    def __init__(self):
        pass

    def plan(self, left_lane_boundary: np.ndarray, right_lane_boundary: np.ndarray):
        """
        Plans a path by finding the midpoint between left and right lane boundaries that are within a specified distance range.

        Inputs:
        - left_lane_boundary: An ndarray of tuples representing the coordinates of the left lane boundary.
        - right_lane_boundary: An ndarray of tuples representing the coordinates of the right lane boundary.

        Outputs:
        - A tuple containing:
          1. A list of midpoints (tuples) calculated between the left and right lane boundaries.
          2. A float representing the calculated curvature of the path based on the x-coordinate differences in the path list.
        """

        def distance(point1: tuple, point2: tuple) -> float:
            # Calculates the Euclidean distance modified by a factor on the y-coordinate difference between two points.
            return math.sqrt((point1[0] - point2[0]) ** 2 + ((point1[1] - point2[1]) * 0.6) ** 2)


        def midpoint(point1: tuple, point2: tuple) -> tuple:
            # Calculates the midpoint between two given points.
            return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)


        if len(left_lane_boundary) == 0 or len(right_lane_boundary) == 0:
            return [], 0

        path = []
        last_right_index = 0

        # Generate path by finding pairs of points that are within a certain distance range and computing their midpoints.
        for i, left_point in enumerate(left_lane_boundary):
            for offset, right_point in enumerate(right_lane_boundary[last_right_index:], start=last_right_index):
                if 19.5 < distance(left_point, right_point) < 24:
                    path.append(midpoint(left_point, right_point))
                    last_right_index = offset
                    break

        curvature = 0
        # Calculate the curvature of the path based on changes in the x-coordinates of the path points.
        if len(path) > 22:
            for i in range(14):
                curvature += abs(path[i+7][0] - path[i+8][0])
        elif len(path) > 8:
            for i in range(len(path) - 8):
                curvature += abs(path[i+7][0] - path[i+8][0])

        return path, curvature