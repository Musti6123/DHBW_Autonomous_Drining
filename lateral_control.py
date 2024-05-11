from __future__ import annotations
import math
import path_planning

import numpy as np






class LateralControl:

    def __init__(self):
        self._car_position = np.array([47, 64])

        self.steering_angle = [0]  # Setze den Lenkwinkel auf 0 Grad zu Beginn


    #definieren vom positiven und negativen Winkel, 90° = pi/2
    # Begrenzung des Winkels



    #Vom auto aus den nähsten Punkt finden
    def find_nearest_point(self,trajectory):
        if len(trajectory) > 0:
            distances = [np.linalg.norm(self._car_position-trajectory) for trajectory in trajectory]
            nearest_index = np.argmin(distances)
            return trajectory[nearest_index]
        return self._car_position


    #Distanz zwischen Auto und nähesten Punkt
    def distance_to_nearest_point(self,nearest_point):
        return np.linalg.norm(self._car_position-nearest_point)


    #Bestimmen des Winkels des Pfades

    def calculate_path_angle(self,nearest_point):
        angle = math.atan2(nearest_point[0]-self._car_position[0], nearest_point[1]-self._car_position[1])

        return math.degrees(angle)

    #pd controll



    # Stanley Formel

    def control(self, trajectory, speed):

        #Prüfen ob speed >0



        nearest_point = self.find_nearest_point(trajectory)
        crosstrack_error = self.distance_to_nearest_point(nearest_point)
        path_angle = self.calculate_path_angle(nearest_point)

        #print (self._car_position)

        delta = path_angle + math.atan(0.8 *crosstrack_error / (-0.0000000002 + speed))

        if delta > math.pi/2:
            delta = math.pi/2
        elif delta < -math.pi/2:
            delta = -math.pi/2

            print(speed)


        return delta




