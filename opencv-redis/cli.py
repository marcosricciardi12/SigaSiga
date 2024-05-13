import cv2
import numpy as np
import redis
import base64

# Conectar a la base de datos Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Ajusta la configuración según tu entorno

def base64_to_image(base64_string):
    decoded_data = np.frombuffer(base64.b64decode(base64_string), np.uint8)
    image = cv2.imdecode(decoded_data, cv2.IMREAD_COLOR)
    return image

if __name__ == '__main__':
    # Leer el fotograma desde Redis
    frame_data = redis_client.get('video_frame')
    if frame_data is not None:
        # Convertir el fotograma de base64 a imagen
        frame_image = base64_to_image(frame_data)
        # Verificar que la imagen no esté vacía y tenga dimensiones válidas
        if frame_image is not None and frame_image.shape[0] > 0 and frame_image.shape[1] > 0:
            # Mostrar la imagen utilizando OpenCV
            cv2.imshow('Frame from Redis', frame_image)
            cv2.waitKey(0)  # Esperar a que se presione una tecla
            cv2.destroyAllWindows()
        else:
            print('La imagen tiene dimensiones no válidas')
    else:
        print('No se encontró ningún fotograma en Redis')