from __future__ import annotations
import math
import os
import sys

import numpy as np


class LongitudinalControl:
    integral = 0.0
    prev_error = 0.0

    max = 0.0
    min = 0.0
    dt = 0.0
    def __init__(self, kp=1.0, ki=0.0, kd=0.0, dt= 0.0):
        self.dt = dt
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.max = max
        self.min = min



    def control(self, speed, target_speed, steering_angle):
      #  self.max = max
      #  self.min = min
        error = target_speed - speed

        proportional = self.kp * error
        self.integral += error * self.dt
        integral = self.ki * self.integral
        derivative = self.kd * (error - self.prev_error) / self.dt

        control_output = proportional + integral + derivative

       # if control_output > self.max:
        #    control_output = self.max
       # elif control_output < self.min:
         #   control_output = self.min

        self.prev_error = error

        if isinstance(control_output, np.ndarray):
            acceleration = np.where(control_output >= 0, control_output, 0.0)
            braking = np.where(control_output < 0, -control_output, 0.0)
        else:
            acceleration = control_output if control_output >= 0 else 0.0
            braking = -control_output if control_output < 0 else 0.0

        return acceleration, braking
      # return control_output

    def predict_target_speed(self, speed, trajectory, steering_angle):
        curvature = np.mean(np.abs(np.gradient(trajectory)))
        reduction_factor = 1.0 - np.clip(curvature * 10, 0.0, 0.9)
        target_speed = speed * reduction_factor

        return target_speed
