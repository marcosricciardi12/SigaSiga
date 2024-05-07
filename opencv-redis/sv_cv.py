import cv2
import redis

# Conectarse a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Capturar la fuente de video HTTP
cap = cv2.VideoCapture('http://192.168.54.142:4747/video')

while True:
    # Leer un frame del video
    ret, frame = cap.read()

    # Convertir el frame a formato de bytes
    _, img_encoded = cv2.imencode('.jpg', frame)
    frame_bytes = img_encoded.tobytes()

    # Guardar el frame en Redis
    r.set('video_frame', frame_bytes)

    # Salir del bucle si se presiona 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar el objeto de captura
cap.release()