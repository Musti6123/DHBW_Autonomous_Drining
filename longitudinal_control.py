from __future__ import annotations
import math
import os
import sys

import numpy as np


class LongitudinalControl:
    integral = 0.0
    prev_error = 0.0

    def __init__(self, kp=1.0, ki=0.0, kd=0.0, dt=0.1, max_speed=70, min_speed=5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.dt = dt
        self.max_speed = max_speed
        self.min_speed = min_speed

    def control(self, speed, target_speed, steering_angle):
        error = target_speed - speed
        proportional = self.kp * error
        self.integral += error * self.dt
        integral = self.ki * self.integral
        derivative = self.kd * (error - self.prev_error) / self.dt
        control_output = proportional + integral + derivative
        adjusted_speed = max(min(control_output + speed, self.max_speed), self.min_speed)

        # Set 'accelerate' and 'brake' depending on the size of the error
        if abs(error) <= 2:
            accelerate = 0  # Let the vehicle roll because it is close enough to the target speed
            brake = 0
        else:
            accelerate = 1 if control_output > 0 else 0
            brake = 1 if control_output < 0 else 0

        self.prev_error = error

        return accelerate, brake


    def predict_target_speed(self, curvature):
        if isinstance(curvature, int):
            if curvature < 5:
                return max(self.max_speed - curvature * 2, 20)  # Minimum 20 with slight curvature
            else:
                return 15  # Braking sharply with high curvature
        return 15
