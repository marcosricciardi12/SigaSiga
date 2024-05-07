import cv2
import numpy as np
import redis

# Conectarse a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

while True:
    # Recuperar el frame almacenado en Redis
    frame_bytes = r.get('video_frame')

    if frame_bytes:
        # Convertir los bytes del frame a formato de imagen
        nparr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Mostrar el frame
        cv2.imshow('Video Reproducido', frame)

    # Salir del bucle si se presiona 'q'
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cerrar las ventanas
cv2.destroyAllWindows()