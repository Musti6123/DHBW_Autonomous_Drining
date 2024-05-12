from __future__ import annotations
import math
import numpy as np

class LateralControl:
    def __init__(self, k=2):
        self._car_position = np.array([47, 68])
        self.steering_angle = 0.0  # Initialize steering angle to 0 degrees
        self.k = k  # Gain parameter for the control law
        self.call_count = 0  # Initialize the count of method calls
        self.points_after = 5

    def find_nearest_point(self, trajectory):
        if len(trajectory) == 0:
            return float('inf'), self._car_position, 0

        trajectory_np = np.array(trajectory)
        distances = np.sqrt((trajectory_np[:, 0] - self._car_position[0]) ** 2 + (trajectory_np[:, 1] - self._car_position[1]) ** 2)

        nearest_index = np.argmin(distances)
        if trajectory_np[nearest_index][0] < self._car_position[0]:
            distances[nearest_index] = -distances[nearest_index]
        return distances[nearest_index], trajectory_np[nearest_index], nearest_index

    def calculate_path_angle(self, nearest_point, points_after):
        dx = points_after[0] - nearest_point[0]

        dy = nearest_point[1] - points_after[1]
        if dx == 0:
            return 0  # Avoid division by zero
        angle = math.atan(dy/dx)  # atan2 is safe for dy=0 or dx=0
        return angle  # Convert radians to degrees

    def control(self, trajectory, speed):
        self.call_count += 1  # Increment the call counter each time the control is called
        if speed <= 0 or self.call_count <= 20:
            return 0  # No steering if the car is not moving or during the first 20 calls

        distance, nearest_point, nearest_index = self.find_nearest_point(trajectory)
        path_angle = 0
        if trajectory:
            if len(trajectory) > nearest_index + self.points_after:
                path_angle = self.calculate_path_angle(nearest_point, trajectory[nearest_index + self.points_after])
            else:
                path_angle = self.calculate_path_angle(nearest_point, trajectory[len(trajectory) - 1])

        # Cross-track error (lateral error)
        cross_track_error = distance

        # Calculate the desired steering angle using the control law
        correction_angle = math.atan(self.k * cross_track_error / speed)
        steering_angle = path_angle + correction_angle  # Convert radians to degrees
        return steering_angle