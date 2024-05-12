from __future__ import annotations
import math
import numpy as np

class LongitudinalControl:
    integral = 0.0
    prev_error = 0.0

    def __init__(self, kp=2, ki=0.4, kd=4, dt=0.1, max_speed=55, min_speed=10):
        # Constructor for the PID controller with default PID coefficients, delta time, and speed limits
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.max_speed = max_speed
        self.min_speed = min_speed

    def control(self, speed, target_speed):
        """
        Calculates the control action to match the current speed to the target speed using PID control.

        Args:
            speed (float): Current speed of the vehicle.
            target_speed (float): Desired speed of the vehicle.

        Returns:
            tuple: Returns a tuple (accelerate, brake) indicating whether to accelerate or brake.
        """

        error = target_speed - speed  # Calculate error between target and current speed
        proportional = self.kp * error  # Calculate proportional term
        self.integral += error * self.dt  # Update integral term
        integral = self.ki * self.integral  # Calculate integral term
        derivative = self.kd * (error - self.prev_error) / self.dt  # Calculate derivative term
        control_output = proportional + integral + derivative  # Sum up PID terms

        # Determine control actions based on the PID output and error margins
        if -10 < error <= 10:
            accelerate = 0  # No acceleration if within error margin
            brake = 0
        else:
            accelerate = 1 if control_output > 0 else 0  # Accelerate if PID output is positive
            brake = 1 if control_output < 0 else 0  # Brake if PID output is negative

        self.prev_error = error  # Store current error for next derivative calculation

        return accelerate, brake

    def predict_target_speed(self, curvature, steering_angle):
        """
        Predicts target speed based on road curvature and steering angle to ensure safe handling.

        Args:
            curvature (float): The curvature of the road.
            steering_angle (float): Current steering angle of the vehicle.

        Returns:
            float: Adjusted target speed considering curvature and steering input.
        """

        # Adjust the speed based on curvature and steering angle
        curvature_effect = max(self.max_speed - curvature * 2, 20)  # Stronger effect from curvature
        steering_effect = max(self.max_speed - abs(math.degrees(steering_angle)) * 0.7, 20)  # Reduce the influence of steering angle

        # Use the lower of two effects to ensure safety
        return max(curvature_effect, self.min_speed)