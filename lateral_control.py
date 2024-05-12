from __future__ import annotations
import math
import numpy as np

class LateralControl:
    def __init__(self, k=0.00005):
        self._car_position = np.array([47, 68])
        self.steering_angle = 0.0  # Initialize steering angle to 0 degrees
        self.k = k  # Gain parameter for the control law

    def find_nearest_point(self, trajectory):
        if len(trajectory) == 0:
            return float('inf'), self._car_position

        trajectory_np = np.array(trajectory)
        distances = np.sqrt((trajectory_np[:, 0] - self._car_position[0]) ** 2 + (trajectory_np[:, 1] - self._car_position[1]) ** 2)
        nearest_index = np.argmin(distances)
        return distances[nearest_index], trajectory_np[nearest_index]

    def calculate_path_angle(self, nearest_point):
        dx = self._car_position[0] - nearest_point[0]
        dy = self._car_position[1] - nearest_point[1]
        if dx == 0:
            return 0  # Avoid division by zero

        angle = math.atan2(dy, dx)  # atan2 is safe for dy=0 or dx=0
        print(math.degrees(angle))
        return math.degrees(angle)  # Convert radians to degrees

    def control(self, trajectory, speed):
        if speed <= 0:
            return 0  # No steering needed if the car is not moving

        distance, nearest_point = self.find_nearest_point(trajectory)
        path_angle = self.calculate_path_angle(nearest_point)

        # Cross-track error (lateral error)
        cross_track_error = distance

        # Calculate the desired steering angle using the control law
        correction_angle = math.atan(self.k * cross_track_error / speed)
        steering_angle = path_angle - math.degrees(correction_angle)  # Convert radians to degrees

        return steering_angle