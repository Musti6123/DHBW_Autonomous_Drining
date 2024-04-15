from __future__ import annotations

import numpy as np
import cv2

class LaneDetection:

    def __init__(self):
        self.debug_img = None

    def detect(self, observation: np.ndarray) -> np.ndarray:
        # Konvertiere das Bild in den HSV-Farbraum
        hsv = cv2.cvtColor(observation, cv2.COLOR_BGR2HSV)

        # Definiere Schwellenwerte für Grautöne
        lower_gray = np.array([0, 0, 0])
        upper_gray = np.array([180, 255, 110])  # Helligkeit bis 110 für Grautöne

        # Erstelle eine Maske, die nur Grau- und Schwarztöne zulässt
        mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)

        # Erkenne die Ränder im gefilterten Bild
        edges = cv2.Canny(mask_gray, 50, 150)

        # Erstelle ein schwarzes Bild der gleichen Größe wie das Originalbild
        black_image = np.zeros_like(observation)

        # Verwende die Hough-Transformation, um Linien im Bild zu erkennen
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=100)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if x2 != x1:
                    slope = (y2 - y1) / (x2 - x1)
                    if slope > 0:
                        # Zeichne rechte Linie in Rot
                        cv2.line(black_image, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    else:
                        # Zeichne linke Linie in Blau
                        cv2.line(black_image, (x1, y1), (x2, y2), (255, 0, 0), 2)

        # Füge am unteren Rand des Bildes einen schwarzen Balken hinzu
        balken_hoehe = 13
        black_image[-balken_hoehe:] = 0

        # Blende einen Kasten in der Mitte des Bildes aus
        mitte_x, mitte_y = (47, 71)
        black_image[mitte_y - 12 // 2:mitte_y + 12 // 2,
        mitte_x - 8 // 2:mitte_x + 8 // 2] = 0

        # Speichere das bearbeitete Bild in debug_img zur Anzeige
        self.debug_img = black_image

        return self.debug_img
