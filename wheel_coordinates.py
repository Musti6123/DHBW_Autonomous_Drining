import cv2
import numpy as np
import matplotlib.pyplot as plt


# Lade das Beispielbild
img = cv2.imread('Car Racing - Lateral Control_screenshot_09.05.2024.png', cv2.IMREAD_GRAYSCALE)

# Definiere den Laplace-Filter
kernel = np.array([[0, 1, 0],
                   [1, -4, 1],
                   [0, 1, 0]])

# Incl. Diagonale
kernel_diag = np.array([[1, 1, 1],
                        [1, -8, 1],
                        [1, 1, 1]])

# Wende Faltung an
# img_laplace = faltung(img, kernel)
# img_laplace_diag = faltung(img, kernel_diag)
img_laplace = faltung_numpy(img, kernel)
img_laplace_diag = faltung_numpy(img, kernel_diag)

# Zeige das Bild
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
axs[0].imshow(img, cmap='gray')
axs[0].set_title('Original')
axs[1].imshow(img_laplace, cmap='gray')
axs[1].set_title('Laplace-Filter')
axs[2].imshow(img_laplace_diag, cmap='gray')
axs[2].set_title('Laplace-Filter (Diagonal)')
plt.show()