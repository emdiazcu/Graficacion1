import cv2
import numpy as np
import math

# --- 1. INICIALIZACIÓN Y CONFIGURACIÓN ---

# Inicializar la captura de video desde la cámara
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: No se puede abrir la cámara.")
    exit()

# Obtener dimensiones del frame (se usarán para el lienzo)
ret, frame = cap.read()
if not ret:
    print("Error: No se pudo leer el frame.")
    exit()
h, w, _ = frame.shape

# Crear un lienzo negro para dibujar sobre él
paint_canvas = np.zeros((h, w, 3), dtype=np.uint8)

# Definir el rango del color rojo en el espacio de color HSV
# El rojo en HSV se encuentra en dos extremos del espectro H (0 y 180)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])
lower_red2 = np.array([170, 120, 70])
upper_red2 = np.array([180, 255, 255])

# Definir la paleta de colores (en formato BGR)
# Cada color es un diccionario con su rectángulo (x, y, w, h) y valor BGR
palette_colors = [
    {'rect': (10, 10, 50, 50), 'color': (0, 0, 255)},   # Rojo
    {'rect': (70, 10, 50, 50), 'color': (0, 255, 0)},   # Verde
    {'rect': (130, 10, 50, 50), 'color': (255, 0, 0)},  # Azul
    {'rect': (190, 10, 50, 50), 'color': (0, 255, 255)}, # Amarillo
    {'rect': (250, 10, 50, 50), 'color': (255, 255, 255)},# Borrador (Blanco, pero lo usaremos para dibujar negro)
]
current_color = palette_colors[0]['color'] # Color inicial del pincel

# Variables para la lógica de dibujo
# Coordenadas previas del pincel (px, py)
px, py = 0, 0
# Umbral de distancia para dibujar (evita líneas accidentales)
distance_threshold = 50

# --- 2. BUCLE PRINCIPAL ---

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear el frame horizontalmente para efecto espejo
    frame = cv2.flip(frame, 1)
    
    # --- 3. DETECCIÓN DEL PINCEL (OBJETO ROJO) ---

    # Convertir el frame de BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Crear máscaras para los dos rangos de rojo
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    # Combinar las dos máscaras
    red_mask = cv2.add(mask1, mask2)

    # Limpiar la máscara para eliminar ruido
    red_mask = cv2.erode(red_mask, None, iterations=2)
    red_mask = cv2.dilate(red_mask, None, iterations=2)

    # Encontrar los contornos del objeto rojo
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # --- 4. LÓGICA DE DIBUJO Y PALETA ---

    if len(contours) > 0:
        # Encontrar el contorno más grande (asumimos que es el pincel)
        brush_contour = max(contours, key=cv2.contourArea)
        
        # Obtener el centro del contorno
        M = cv2.moments(brush_contour)
        if M["m00"] > 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Dibujar un círculo para visualizar el centro del pincel
            cv2.circle(frame, (cx, cy), 10, (100, 100, 100), 2)

            # --- Interacción con la Paleta de Colores ---
            if cy < 70: # Si el pincel está en la zona de la paleta
                for item in palette_colors:
                    x, y, w_rect, h_rect = item['rect']
                    if x < cx < x + w_rect:
                        current_color = item['color']
                        # Si es el borrador, cambiamos a negro para "borrar"
                        if current_color == (255, 255, 255):
                            current_color = (0,0,0)

            # --- Lógica de Dibujo con Distancia Euclidiana ---
            if px == 0 and py == 0:
                # Si es la primera vez que detectamos el pincel, guardamos su posición
                px, py = cx, cy
            
            # Calcular la distancia euclidiana entre el punto actual y el anterior
            distance = math.hypot(cx - px, cy - py)
            
            # Si la distancia es menor que el umbral, dibujamos
            if distance < distance_threshold:
                # Dibujar una línea en el lienzo negro
                cv2.line(paint_canvas, (px, py), (cx, cy), current_color, 5)
            
            # Actualizar las coordenadas previas
            px, py = cx, cy

    else:
        # Si no se detecta el pincel, reiniciamos las coordenadas previas
        # Esto evita que se dibuje una línea larga cuando el pincel reaparece
        px, py = 0, 0

    # --- 5. VISUALIZACIÓN ---

    # Combinar el lienzo de dibujo con el frame de la cámara
    # Primero, creamos una máscara inversa del lienzo (donde NO hay dibujo)
    gray_canvas = cv2.cvtColor(paint_canvas, cv2.COLOR_BGR2GRAY)
    _, inv_mask = cv2.threshold(gray_canvas, 10, 255, cv2.THRESH_BINARY_INV)
    # Usamos la máscara para "cortar" el área de dibujo del frame de la cámara
    frame_bg = cv2.bitwise_and(frame, frame, mask=inv_mask)
    # Sumamos el fondo cortado con nuestro lienzo de dibujo
    result = cv2.add(frame_bg, paint_canvas)

    # Dibujar la paleta de colores sobre el resultado final
    for item in palette_colors:
        x, y, w_rect, h_rect = item['rect']
        cv2.rectangle(result, (x, y), (x + w_rect, y + h_rect), item['color'], -1)
        # Borde negro para el borrador para que sea visible
        if item['color'] == (255, 255, 255):
            cv2.rectangle(result, (x, y), (x + w_rect, y + h_rect), (0,0,0), 2)


    cv2.imshow('Pizarra Virtual', result)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 6. LIBERAR RECURSOS ---
cap.release()
cv2.destroyAllWindows()