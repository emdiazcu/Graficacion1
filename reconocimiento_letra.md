<div align="center">

---

# INSTITUTO TECNOLÓGICO DE MORELIA  

## Reconocimiento de Letras con Visión por Computadora

### Ingeniería en Sistemas Computacionales  
### Graficación

---

### Alumno:
**Díaz Curiel Emiliano**

### No. Control:
***22121369***

---
## Sistema de Reconocimiento de Letras usando OpenCV + MediaPipe

</div>

<div align="justify">

Este proyecto implementa un sistema capaz de **detectar una mano en tiempo real**, identificar sus **puntos clave (landmarks)** y reconocer algunas letras del lenguaje de señas mediante relaciones geométricas entre los dedos.

Se utilizan herramientas modernas como:

- **OpenCV** – Procesamiento y visualización de video  
- **MediaPipe Hands** – Detección de mano y sus 21 landmarks  
- **NumPy** – Cálculo matemático y vectorial  

A continuación, se explica el código por secciones, junto con el fragmento correspondiente.

---

## Importación de Librerías

En esta sección importamos las librerías necesarias para:

- Manipular video (OpenCV)  
- Detectar manos (MediaPipe)  
- Calcular distancias entre dedos (NumPy)

```python
import cv2
import mediapipe as mp
import numpy as np
```

---

## Inicialización de MediaPipe Hands

Se configura el detector de manos de MediaPipe, definiendo:

- Confianza mínima para detección
- Confianza mínima para seguimiento
- Objetos auxiliares para dibujar los landmarks

```python
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
```

---

## Función `reconocer_letra()`

Esta función recibe los landmarks detectados y realiza:

- Conversión de coordenadas normalizadas → píxeles  
- Cálculo de distancias entre dedos  
- Visualización de puntos y líneas  
- Lógica de reconocimiento para letras A, B y C  

```python
def reconocer_letra(hand_landmarks, frame):
    h, w, _ = frame.shape
    
    # Obtener coordenadas en píxeles
    dedos = [(int(hand_landmarks.landmark[i].x * w),
              int(hand_landmarks.landmark[i].y * h)) for i in range(21)]
    
    pulgar, indice, medio, anular, meñique = dedos[4], dedos[8], dedos[12], dedos[16], dedos[20]

    # Dibujar landmarks y números
    for i, (x, y) in enumerate(dedos):
        cv2.circle(frame, (x, y), 5, (0, 234, 0), -1)
        cv2.putText(frame, str(i), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    # Mostrar coordenadas y línea
    cv2.putText(frame, f'({int(pulgar[0])}, {int(pulgar[1])})',
                (pulgar[0], pulgar[1] - 15),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (245, 0, 0), 2)
    
    cv2.line(frame, pulgar, indice, (244, 34, 12), 2)

    # Calcular distancias
    distancia_pulgar_indice = np.linalg.norm(np.array(pulgar) - np.array(indice))
    distancia_indice_medio = np.linalg.norm(np.array(indice) - np.array(medio))

    # Mostrar distancia
    cv2.putText(frame, f'({distancia_pulgar_indice})',
                (pulgar[0] - 40, pulgar[1] - 45),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Lógica de reconocimiento
    if distancia_pulgar_indice < 30 and distancia_indice_medio > 50:
        return "A"
    elif indice[1] < medio[1] < anular[1] < meñique[1]:
        return "B"
    elif distancia_pulgar_indice > 50 and distancia_indice_medio > 50:
        return "C"

    return "Desconocido"
```

---

## Captura de Video

Aquí se abre la cámara y se inicia un ciclo de lectura continua de frames.

```python
cap = cv2.VideoCapture(1)
```

---

## Procesamiento de la Mano y Reconocimiento

En cada frame:

- Se convierte a RGB  
- Se detectan manos con MediaPipe  
- Se dibujan puntos y conexiones  
- Se determina la letra detectada  

```python
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            letra_detectada = reconocer_letra(hand_landmarks, frame)

            cv2.putText(frame, f"Letra: {letra_detectada}", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 255, 0), 2)
```

---

## Visualización en Pantalla

Se muestra el frame procesado en una ventana llamada "Reconocimiento de Letras".

```python
    cv2.imshow("Reconocimiento de Letras", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
```

---

## Liberación de Recursos

Al finalizar el programa se liberan los recursos utilizados.

```python
cap.release()
cv2.destroyAllWindows()
```

</div>
