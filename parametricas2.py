import numpy as np
import cv2

# Definir los parámetros de la circunferencia
r = 100  # radio
h = 250  # centro en x
k = 250  # centro en y
num_frames = 100  # número de frames en la animación
t_vals = np.linspace(0, 2*np.pi, num_frames)  # valores del parámetro t

# Crear una ventana para mostrar la animación
cv2.namedWindow('Animación Circunferencia', cv2.WINDOW_AUTOSIZE)

# Animar la circunferencia
for i in range(len(t_vals)):
    t = t_vals[i]
    
    # Calcular las coordenadas del punto en la circunferencia
    x = int(h + r * np.cos(t))
    y = int(k + r * np.sin(t))
    
    # Crear una imagen en blanco
    frame = np.ones((500, 500, 3), dtype=np.uint8) * 255
    
    # Dibujar la circunferencia
    cv2.circle(frame, (h, k), r, (0, 0, 0), 2)
    
    # Dibujar el punto en movimiento
    cv2.circle(frame, (x, y), 10, (0, 0, 255), -1)
    
    # Mostrar el frame en la ventana
    cv2.imshow('Animación Circunferencia', frame)
    
    # Esperar un corto tiempo para crear la animación (ajustar velocidad)
    cv2.waitKey(50)
    
# Cerrar la ventana cuando la animación termine
cv2.destroyAllWindows()