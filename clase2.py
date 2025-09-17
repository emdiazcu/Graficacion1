import numpy as np
import cv2 as cv

img = np.ones((500, 500), dtype=np.uint8) * 255
x = 1
y=101
while x and y < 500:
    for i in range(x,y):
        for j in range(x,y):                    
            img[i, j]=100
    x=x+100
    y=y+100
# Muestra la imagen en una ventana con el título 'img'. 
cv.imshow('img', img)

# Espera a que el usuario presione cualquier tecla para continuar.
cv.waitKey(0)

# Cierra todas las ventanas creadas por OpenCV.
cv.destroyAllWindows()