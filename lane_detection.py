from __future__ import annotations

import numpy as np
import cv2
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

class LaneDetection:

    def __init__(self):
        self.debug_img = None




    def detect(self, observation: np.ndarray) -> np.ndarray:





        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(observation, cv2.COLOR_BGR2HSV)

        # Define threshold values for gray tones
        lower_gray = np.array([0, 0, 0])
        upper_gray = np.array([180, 255, 110])  # Brightness up to 100 for gray tones

        # Create a mask that only allows gray and black tones
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

        # Recognize the edges in the filtered image
        edges = cv2.Canny(mask_gray, 50, 150)

        # Create a black image of the same size as the original image
        black_image = np.zeros_like(observation)

        # Draw the white borders on the black image
        black_image[edges == 255] = (255, 255, 255)

        # Add a black bar at the bottom of the image
        balken_hoehe = 13  # Height of the bar in pixels
        black_image[-balken_hoehe:] = 0  # Set the lower 'balken_hoehe' pixels to black

        # Hide a box in the center of the image
        mitte_x, mitte_y = (47,71)
        black_image[mitte_y - 12 // 2:mitte_y + 12 // 2,
        mitte_x - 8 // 2:mitte_x + 8 // 2] = 0

        def connectPoints(coordinate1: tuple, coordinate2: tuple):
            cv2.line(black_image, coordinate1, coordinate2, (255, 255, 255), 1)


        for i in range(10):
            if np.array_equal(black_image[64, 42+i], [255, 255, 255]):
                for j in range(14):
                    if np.array_equal(black_image[64+j, 42], [255, 255, 255]):
                        connectPoints((42+i, 62), (42, 64+j))
                        break
                    if np.array_equal(black_image[64+j, 51], [255, 255, 255]):
                        connectPoints((42+i, 64), (51, 64+j))
                        break
                for j in range(10):
                    if np.array_equal(black_image[78, 42+j], [255, 255, 255]):
                        connectPoints((42+i, 64), (42+j, 78))

        visited = np.zeros((96, 96), dtype=bool)
        left_line_coordinates = []
        right_line_coordinates = []

        def dfs(y, x, side):
            # Base case: Check the borders and whether the pixel has already been visited or is not white
            if y < 0 or y >= 96 or x < 0 or x >= 96 or visited[y, x] or not np.array_equal(black_image[y, x], [255, 255, 255]):
                return

            # Mark this pixel as visited
            visited[y, x] = True
            if side == 'left':
                left_line_coordinates.append((x, y))
            if side == 'right':
                right_line_coordinates.append((x, y))

            # Recursive search in a 5x5 area around the pixel
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    dfs(y + dy, x + dx, side)

        left = 0
        right = 0

        for i in range(47):
            if np.array_equal(black_image[82, 47-i], [255, 255, 255]):
                if left == 0:
                    dfs(82, 47-i, 'left')
                    left = 1
            if np.array_equal(black_image[64, 57-i], [255, 255, 255]):
                if left == 1:
                    if len(left_line_coordinates) < 15:
                        dfs(64, 57-i, 'left')
                        left = 2
            if np.array_equal(black_image[82, 48+i], [255, 255, 255]):
                if right == 0:
                    dfs(82, 48+i, 'right')
                    right = 1
            if np.array_equal(black_image[64, 38+i], [255, 255, 255]):
                if right == 1:
                    if len(right_line_coordinates) < 15:
                        dfs(64, 38+i, 'right')
                        right = 2
            if right == 2 & left == 2:
                break

        if len(left_line_coordinates) == 0:
            left_line_coordinates = right_line_coordinates.copy()
            right_line_coordinates = []
            if len(left_line_coordinates) > 0:
                for i in range(96-left_line_coordinates[0][1]):
                    if np.array_equal(black_image[82, left_line_coordinates[0][1]+i], [255, 255, 255]):
                        dfs(82, left_line_coordinates[0][1]+i, 'right')
                if len(left_line_coordinates) == 0:
                    for i in range(82):
                        if np.array_equal(black_image[82-i, 0], [255, 255, 255]):
                            dfs(82-i, 96, 'right')

        if len(right_line_coordinates) == 0:
            right_line_coordinates = left_line_coordinates.copy()
            left_line_coordinates = []
            if len(right_line_coordinates) > 0:
                for i in range(right_line_coordinates[0][1]):
                    if np.array_equal(black_image[82, right_line_coordinates[0][1]-i], [255, 255, 255]):
                        dfs(82, right_line_coordinates[0][1]-i, 'left')
                if len(right_line_coordinates) == 0:
                    for i in range(82):
                        if np.array_equal(black_image[82-i, 0], [255, 255, 255]):
                            dfs(82-i, 0, 'left')

        if len(right_line_coordinates) == 0:
            for i in range(94):
                if np.array_equal(black_image[35, 94-i], [255, 255, 255]):
                    dfs(35, i, 'right')

        if len(left_line_coordinates) == 0:
            for i in range(94):
                    if np.array_equal(black_image[35, i], [255, 255, 255]):
                        dfs(35, i, 'left')




        for i in range(len(left_line_coordinates)):
            black_image[left_line_coordinates[i][1]][left_line_coordinates[i][0]] = [0, 255, 0]

        for i in range(len(right_line_coordinates)):
            black_image[right_line_coordinates[i][1]][right_line_coordinates[i][0]] = [255, 0, 0]



        self.debug_img = black_image

        return [left_line_coordinates, right_line_coordinates]