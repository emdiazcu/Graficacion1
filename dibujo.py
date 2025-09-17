import cv2 as cv 
import numpy as np

video = cv.VideoCapture(0)

ret, cuadro = video.read()
lienzo = np.zeros_like(cuadro)

u_bajo = np.array([0, 150, 50])
u_alto = np.array([])

punto_anterior = None
umbral_distancia = 50

while True:
    ret,cuadro = video.read()
    if not ret:
        break
    
