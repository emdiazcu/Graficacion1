import cv2
import mediapipe as mp
import numpy as np
import math

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
# Modificación: Se configura para detectar un máximo de 2 manos
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Captura de video
# Elige 0 para la cámara integrada o 1, 2, etc., para cámaras externas.
cap = cv2.VideoCapture(1) 

# --- Posición y color del cuadrado ---
# Puedes cambiar estas coordenadas si quieres que el cuadrado aparezca en otro lugar.
CUADRADO_X, CUADRADO_Y = 150, 150 
CUADRADO_COLOR = (0, 255, 0) # Verde

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear el frame horizontalmente para un efecto espejo
    frame = cv2.flip(frame, 1)

    # Convertir a RGB para MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen
    results = hands.process(frame_rgb)

    # Dibujar los resultados
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
        # Se detectaron dos manos
        hand1_landmarks = results.multi_hand_landmarks[0]
        hand2_landmarks = results.multi_hand_landmarks[1]

        # Dibujar los esqueletos de ambas manos
        mp_drawing.draw_landmarks(frame, hand1_landmarks, mp_hands.HAND_CONNECTIONS)
        mp_drawing.draw_landmarks(frame, hand2_landmarks, mp_hands.HAND_CONNECTIONS)

        # --- Cálculo de la distancia ---
        h, w, _ = frame.shape

        # Obtener las coordenadas del dedo índice (landmark 8) de cada mano
        # Landmark 8 es la punta del dedo índice
        punta_indice_1 = hand1_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        punta_indice_2 = hand2_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Convertir coordenadas normalizadas (0 a 1) a coordenadas en píxeles
        x1, y1 = int(punta_indice_1.x * w), int(punta_indice_1.y * h)
        x2, y2 = int(punta_indice_2.x * w), int(punta_indice_2.y * h)

        # Calcular la distancia euclidiana
        distancia = int(math.hypot(x2 - x1, y2 - y1))

        # --- Dibujar en pantalla ---

        # 1. Dibujar una línea entre los dos dedos índice
        cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)
        # 2. Dibujar círculos en las puntas de los dedos índice
        cv2.circle(frame, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (0, 0, 255), cv2.FILLED)

        # 3. Dibujar el cuadrado cuyo tamaño depende de la distancia
        tamaño_cuadrado = distancia
        # El punto final se calcula sumando el tamaño al punto inicial
        punto_final = (CUADRADO_X + tamaño_cuadrado, CUADRADO_Y + tamaño_cuadrado)
        cv2.rectangle(frame, (CUADRADO_X, CUADRADO_Y), punto_final, CUADRADO_COLOR, cv2.FILLED)

        # 4. Mostrar el valor de la distancia en la pantalla
        cv2.putText(frame, f'Distancia: {distancia}px', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        # Mensaje por si no se detectan dos manos
        cv2.putText(frame, 'Muestra dos manos', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)


    # Mostrar el video
    cv2.imshow("Reconocimiento de Letras", frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()