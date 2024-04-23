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
                left_line_coordinates.append((y, x))
            if side == 'right':
                right_line_coordinates.append((y, x))

            # Rekursive Suche in einem 5x5 Bereich um den Pixel herum
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
                if len(left_line_coordinates) == 0:
                    for i in range(82):
                        if np.array_equal(black_image[82-i, 0], [255, 255, 255]):
                            dfs(82-i, 0, 'left')






        for i in range(len(left_line_coordinates)):
            black_image[left_line_coordinates[i][0]][left_line_coordinates[i][1]] = [0, 255, 0]

        for i in range(len(right_line_coordinates)):
            black_image[right_line_coordinates[i][0]][right_line_coordinates[i][1]] = [255, 0, 0]


        #print(black_image[48][14])
        # Speichere das bearbeitete Bild in debug_img zur Anzeige
        self.debug_img = black_image

        return self.debug_img