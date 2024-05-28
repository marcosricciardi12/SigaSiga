import redis
import cv2
import numpy as np
import base64

# Configuración de la conexión a Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def get_frame_from_redis(key):
    # Obtener el frame almacenado en Redis
    encoded_frame = r.get(key)
    if encoded_frame is None:
        print("No frame found in Redis for the given key.")
        return None

    # Decodificar el frame de base64
    webp_frame = base64.b64decode(encoded_frame)

    # Convertir los bytes del frame WebP a una matriz de imagen que OpenCV pueda usar
    image_array = np.frombuffer(webp_frame, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image

def main():
    video_source_key = "video_frame"
    
    while True:
        # Obtener el frame desde Redis
        frame = get_frame_from_redis(video_source_key)
        if frame is None:
            return

        # Mostrar el frame usando OpenCV
        cv2.imshow("Frame from Redis", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()