import cv2
import numpy as np
import math

# Crear lienzo
w, h = 500, 500
cx, cy = w // 2, h // 2   # centro de rotación
img = np.zeros((h, w, 3), dtype=np.uint8)

# Definir un cuadrado alrededor del centro
square = [
    (cx - 100, cy - 100),
    (cx + 100, cy - 100),
    (cx + 100, cy + 100),
    (cx - 100, cy + 100)
]

theta = 0
while True:
    frame = img.copy()

    # Calcular los nuevos puntos aplicando rotación
    rotated_pts = []
    for (j, i) in square:  # ojo: (j,i) porque usamos x=j, y=i
        new_x = int((j - cx) * math.cos(theta) - (i - cy) * math.sin(theta) + cx)
        new_y = int((j - cx) * math.sin(theta) + (i - cy) * math.cos(theta) + cy)
        rotated_pts.append((new_x, new_y))

    # Dibujar el cuadrado rotado
    cv2.polylines(frame, [np.array(rotated_pts, np.int32)], True, (0,255,0), 2)

    # Mostrar frame
    cv2.imshow("Rotacion Parametrica", frame)

    theta += 0.02  # Incrementa el ángulo (velocidad de rotación)

    # salir con tecla q
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
