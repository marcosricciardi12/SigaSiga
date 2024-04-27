import cv2
import numpy as np

# URL del video HTTP
video_url = 'http://192.168.54.139:4747/video'
# video_url = 'http://localhost:5000/video_feed'
# Inicia la captura de video desde la URL
cap = cv2.VideoCapture(video_url)

# Verifica si la captura de video se ha iniciado correctamente
if not cap.isOpened():
    print("Error: No se pudo abrir la captura de video.")
    exit()

# Bucle para leer y mostrar los fotogramas del video
while True:
    # Lee un fotograma del video
    ret, frame = cap.read()

    # Verifica si se ha podido leer correctamente el fotograma
    if not ret:
        print("Error: No se pudo leer el fotograma.")
        break

    # Muestra el fotograma en una ventana
    cv2.imshow('Video', frame)

    # Espera 30 milisegundos y verifica si se presiona la tecla 'q' para salir
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# Libera la captura de video y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()