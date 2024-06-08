import time
import cv2
import numpy as np
import redis
import base64

# Conectar a la base de datos Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)  # Ajusta la configuración según tu entorno

def base64_to_image(base64_string):
    decoded_data = np.frombuffer(base64_string, np.uint8)
    image = cv2.imdecode(decoded_data, cv2.IMREAD_COLOR)
    return image


if __name__ == '__main__':
    # Leer el fotograma desde Redis
    while True:
        time.sleep(1/30)
        frame_data = redis_client.get('ScchtzMp2NvTR2D6UGkME3-socket_video_sources-xWa47hBH9sBXKxJIAAAH') #bytes
        # print(frame_data[:30])
        if frame_data is not None:
            # Convertir el fotograma de base64 a imagen
            frame_image = base64_to_image(frame_data)
            # Verificar que la imagen no esté vacía y tenga dimensiones válidas
            if frame_image is not None and frame_image.shape[0] > 0 and frame_image.shape[1] > 0:
                # Mostrar la imagen utilizando OpenCV
                cv2.imshow('Frame from Redis', frame_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                print('La imagen tiene dimensiones no válidas')
        else:
            print('No se encontró ningún fotograma en Redis')
cv2.waitKey(0)  # Esperar a que se presione una tecla
cv2.destroyAllWindows()