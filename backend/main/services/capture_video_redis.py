import redis
import cv2
import os
import time

def capture_video_source(redis_db, video_source_key, video_url, event_id):
    capture = cv2.VideoCapture(video_url)

    # Obtener el FPS del video original
    fps = capture.get(cv2.CAP_PROP_FPS)
    wait_time = 1/fps
    print(fps)
    while not int(redis_db.get(f'{event_id}-stop')):
        # Obtener el tiempo de inicio para calcular el tiempo de espera
        start_time = time.time()

        # Leer un frame del video
        ret, frame = capture.read()

        if ret:
            # Hacer operaciones adicionales aquí si es necesario

            # Mostrar el frame
            _, img_encoded = cv2.imencode('.jpg', frame)
            frame_bytes = img_encoded.tobytes()

            # Guardar el frame en Redis
            redis_db.set(video_source_key, frame_bytes)


            # Calcular el tiempo de espera en función del FPS
        else:
            break
        end_time = time.time()

        # # Calcular el tiempo transcurrido
        elapsed_time = end_time - start_time
        sleep_time = (wait_time - elapsed_time)
        # print(wait_time, elapsed_time, sleep_time)
        if sleep_time >= 0 : time.sleep(sleep_time)

        # print("Tiempo transcurrido:", elapsed_time, "segundos")

    # Liberar el objeto de captura y cerrar las ventanas
    capture.release()
    cv2.destroyAllWindows()
    os._exit(0)