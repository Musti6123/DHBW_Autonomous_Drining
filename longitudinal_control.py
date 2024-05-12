from __future__ import annotations
import math
import numpy as np

class LongitudinalControl:
    integral = 0.0
    prev_error = 0.0

    def __init__(self, kp=2, ki=0.4, kd=4, dt=0.1, max_speed=70, min_speed=10):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.max_speed = max_speed
        self.min_speed = min_speed

    def control(self, speed, target_speed):
        error = target_speed - speed
        proportional = self.kp * error
        self.integral += error * self.dt
        integral = self.ki * self.integral
        derivative = self.kd * (error - self.prev_error) / self.dt
        control_output = proportional + integral + derivative
        adjusted_speed = max(min(control_output + speed, self.max_speed), self.min_speed)

        # Set 'accelerate' and 'brake' depending on the size of the error
        if abs(error) <= 10 and abs(error) > -10:
            accelerate = 0  # Let the vehicle roll because it is close enough to the target speed
            brake = 0
        else:
            accelerate = 1 if control_output > 0 else 0
            brake = 1 if control_output < 0 else 0

        self.prev_error = error

        return accelerate, brake

    def predict_target_speed(self, curvature, steering_angle):
        # Adjust the speed based on curvature and steering angle
        curvature_effect = max(self.max_speed - curvature * 2, 20)  # Stronger effect from curvature
        steering_effect = max(self.max_speed - abs(math.degrees(steering_angle)) * 0.5, 20)  # Reduce the influence of steering angle

        # Use the lower of two effects to ensure safety
        return max(curvature_effect, self.min_speed)
