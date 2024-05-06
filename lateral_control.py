from __future__ import annotations
import math
import path_planning

import numpy as np




class LateralControl:

    def __init__(self):
        self._car_position = np.array([48, 64])
    pass

    #definieren vom positiven und negativen Winkel, 90° = pi/2

    #Vom auto aus den nähsten Punkt finden
    def find_nearest_point(self,trajectory):
        distances = [np.linalg.norm(self._car_position-trajectory) for trajectory in trajectory]
        nearest_index = np.argmin(distances)
        return trajectory[nearest_index]


    #Distanz zwischen Auto und nähesten Punkt
    def distance_to_nearest_point(self,nearest_point):
        return np.linalg.norm(self._car_position-nearest_point)


    #Bestimmen des Winkels des Pfades

    def calculate_path_angle(self,nearest_point):
        angle = math.atan2(nearest_point[1]-self._car_position[1], nearest_point[0]-self._car_position[0])
        return math.degrees(angle)

    # Stanley Formel

    def control(self, trajectory, speed):

        #Prüfen ob speed >0



        nearest_point = self.find_nearest_point(trajectory)
        crosstrack_error = self.distance_to_nearest_point(nearest_point)
        path_angle = self.calculate_path_angle(nearest_point)
        delta = path_angle + math.atan(crosstrack_error / speed)
        return delta




