import cv2
import time
import redis

# Conectarse a Redis
r = redis.Redis(host='localhost', port=6379, db=0)
# Capturar la fuente de video HTTP
cap = cv2.VideoCapture('http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4')

# Obtener el FPS del video original
fps = cap.get(cv2.CAP_PROP_FPS)
wait_time = 1/fps
print(fps)
while True:
    # Obtener el tiempo de inicio para calcular el tiempo de espera
    start_time = time.time()

    # Leer un frame del video
    ret, frame = cap.read()

    if ret:
        # Hacer operaciones adicionales aquí si es necesario

        # Mostrar el frame
        _, img_encoded = cv2.imencode('.jpg', frame)
        frame_bytes = img_encoded.tobytes()

        # Guardar el frame en Redis
        r.set('video_frame', frame_bytes)


        # Calcular el tiempo de espera en función del FPS
    else:
        break

    end_time = time.time()

    # Calcular el tiempo transcurrido
    elapsed_time = end_time - start_time
    sleep_time = (wait_time - elapsed_time)
    print(wait_time, elapsed_time, sleep_time)
    if sleep_time >= 0 : time.sleep(sleep_time)

    # print("Tiempo transcurrido:", elapsed_time, "segundos")

# Liberar el objeto de captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()
