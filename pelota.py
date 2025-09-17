import cv2
import numpy as np

# Dimensiones de la ventana
ancho, alto = 640, 480

# Crear ventana
cv2.namedWindow("Animacion", cv2.WINDOW_AUTOSIZE)

# Posicion inicial
pos_pelota = np.array([100, 100])
radio_pelota = 20
velocidad = np.array([5, 3])

# Color de la pelotita (azul, verde, rojo)
color_pelota = (255, 0, 0)

# rastrear si la pelota ha rebotado
ha_rebotado = False

# Bucle de animacion
while True:
    # Crear fondo negro
    fotograma = np.zeros((alto, ancho, 3), dtype=np.uint8)
    
    # Dibujar pelotita
    cv2.circle(fotograma, tuple(pos_pelota), radio_pelota, color_pelota, -1)
    
    # Actualizar posicion de la pelota
    pos_pelota += velocidad
    
    # Comprobar colisiones y cambiar direccion
    if pos_pelota[0] - radio_pelota <= 0 or pos_pelota[0] + radio_pelota >= ancho:
        velocidad[0] = -velocidad[0]
        

    if pos_pelota[1] - radio_pelota <= 0 or pos_pelota[1] + radio_pelota >= alto:
        velocidad[1] = -velocidad[1]
         
    
    # Restablecer el estado de rebote 
    if radio_pelota < pos_pelota[0] < ancho - radio_pelota and radio_pelota < pos_pelota[1] < alto - radio_pelota:
        ha_rebotado = False
    
    # Mostrar imagen
    cv2.imshow("Animacion", fotograma)

    # Salir al presionar 'Esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Cerrar todas las ventanas de OpenCV
cv2.destroyAllWindows()