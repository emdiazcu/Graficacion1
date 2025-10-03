import numpy as np
import cv2

# Definir los parámetros iniciales
width, height = 1000, 1000
img = np.ones((height, width, 3), dtype=np.uint8) * 255

# Parámetros de la curva de tu imagen
a, b = 250, 100 # Puedes jugar con estos valores

# Centro de la imagen
center_x, center_y = width // 2, height // 2

# Parámetros de la animación
theta = 0
theta_increment = 0.05

while True:
    # Limpiar la imagen en cada frame para la animación
    img = np.ones((width, height, 3), dtype=np.uint8) * 255
    
    # Dibujar la curva completa desde 0 hasta el ángulo actual 'theta'
    for t in np.arange(0, theta, theta_increment):
        
        # --- CÁLCULO CON TUS ECUACIONES ---
        # Asegurarse de que b no sea cero para evitar división por cero
        if b == 0: b = 1e-6 # Un valor muy pequeño para evitar el error
        
        x_raw = (a - b) * np.cos(t) + np.cos(t * (a / b)) - 1
        y_raw = (a - b) * np.sin(t) - (np.sin(t * (a / b)) - 1)
        
        # Centrar la figura en la pantalla
        x = int(center_x + x_raw)
        y = int(center_y + y_raw)
        # --- FIN DEL CÁLCULO ---
        
        # Dibujar un punto en la posición calculada
        cv2.circle(img, (x, y), 3, (0, 0, 0), -1)

    # Mostrar la imagen
    cv2.imshow("Animacion con tus Ecuaciones", img)
    
    # Incrementar el ángulo para el siguiente frame
    theta += theta_increment
    
    # Salir con la tecla 'ESC'
    if cv2.waitKey(30) & 0xFF == 27:
        break

# Cerrar la ventana al finalizar
cv2.destroyAllWindows()