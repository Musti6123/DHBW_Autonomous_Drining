from __future__ import annotations

import numpy as np
import cv2
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

class LaneDetection:

    def __init__(self):
        self.debug_img = None




    def detect(self, observation: np.ndarray) -> np.ndarray:





        # Konvertiere das Bild in den HSV-Farbraum
        hsv = cv2.cvtColor(observation, cv2.COLOR_BGR2HSV)

        # Definiere Schwellenwerte für Grautöne
        lower_gray = np.array([0, 0, 0])
        upper_gray = np.array([180, 255, 110])  # Helligkeit bis 100 für Grautöne

        # Erstelle eine Maske, die nur Grau- und Schwarztöne zulässt
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

        # Erkenne die Ränder im gefilterten Bild
        edges = cv2.Canny(mask_gray, 50, 150)

        # Erstelle ein schwarzes Bild der gleichen Größe wie das Originalbild
        black_image = np.zeros_like(observation)

        # Zeichne die weißen Ränder auf das schwarze Bild
        black_image[edges == 255] = (255, 255, 255)





        # Füge am unteren Rand des Bildes einen schwarzen Balken hinzu
        balken_hoehe = 13  # Höhe des Balkens in Pixeln
        black_image[-balken_hoehe:] = 0  # Setze die unteren 'balken_hoehe' Pixel auf Schwarz

        # Blende einen Kasten in der Mitte des Bildes aus
        mitte_x, mitte_y = (47,71)
        black_image[mitte_y - 12 // 2:mitte_y + 12 // 2,
        mitte_x - 8 // 2:mitte_x + 8 // 2] = 0

        connected = 0

        def connectPoints(coordinate1: tuple, coordinate2: tuple):
            cv2.line(black_image, coordinate1, coordinate2, (255, 255, 255), 1)
            connected = 1


        for i in range(10):
            if np.array_equal(black_image[64, 42+i], [255, 255, 255]):
                for j in range(14):
                    if np.array_equal(black_image[64+j, 42], [255, 255, 255]):
                        connectPoints((42+i, 64), (42, 64+j))
                        break
                    if np.array_equal(black_image[64+j, 51], [255, 255, 255]):
                        connectPoints((42+i, 64), (51, 64+j))
                        break
                for j in range(10):
                    if np.array_equal(black_image[78, 42+j], [255, 255, 255]):
                        connectPoints((42+i, 64), (42+j, 78))
        if connected == 0:
            for j in range(14):  # Seitenhöhen der Box
                if np.array_equal(black_image[64+j, 42], [255, 255, 255]):
                    for i in range(10):
                        if np.array_equal(black_image[78, 42+i], [255, 255, 255]):
                            connectPoints((42, 64+j), (42+i, 78))
                    if connected == 0:
                        for i in range(14):
                            if np.array_equal(black_image[64+i, 51], [255, 255, 255]):
                                connectPoints((42, 64+j), (51, 64+i))
                if np.array_equal(black_image[64+j, 51], [255, 255, 255]):
                    for i in range(10):
                        if np.array_equal(black_image[78, 42+i], [255, 255, 255]):
                            connectPoints((51, 64+j), (42+i, 78))

        visited = np.zeros((96, 96), dtype=bool)
        left_line_coordinates = []
        right_line_coordinates = []

        def dfs(y, x, side):
            # Basisfall: Überprüfe die Grenzen und ob der Pixel bereits besucht wurde oder nicht weiß ist
            if y < 0 or y >= 96 or x < 0 or x >= 96 or visited[y, x] or not np.array_equal(black_image[y, x], [255, 255, 255]):
                return

            # Markiere diesen Pixel als besucht
            visited[y, x] = True
            if side == 'left':
                left_line_coordinates.append((x, y))
                black_image[y, x] = [255,0,0]
            if side == 'right':
                right_line_coordinates.append((x, y))
                black_image[y, x] = [0,255,0]

            # Rekursive Suche in einem 5x5 Bereich um den Pixel herum
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    dfs(y + dy, x + dx, side)

        left = 0
        right = 0

        for i in range(90):
            if left == 0 or right == 0:
                for j in range(49):
                    if left == 0 or right == 0:
                        if np.array_equal(black_image[90-i, 47+j], [255, 255, 255]):
                            if right == 0:
                                dfs(90-i, 47+j, 'right')
                                right = 1
                            elif left == 0:
                                dfs(90-i, 47+j, 'left')
                                left = 1
                        if np.array_equal(black_image[90-i, 47-j], [255, 255, 255]):
                            if left == 0:
                                dfs(90-i, 47-j, 'left')
                                left = 1
                            elif right == 0:
                                dfs(90-i, 47-j, 'right')
                                right = 1
                        if len(left_line_coordinates) < 15:
                            left = 0
                        if len(right_line_coordinates) < 15:
                            right = 0
                    else:
                        break
            else:
                break

        print(left, right)










        self.debug_img = black_image

        return [left_line_coordinates, right_line_coordinates]