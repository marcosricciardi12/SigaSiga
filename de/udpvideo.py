import cv2
import numpy as np
import subprocess
import datetime
import time

# Función para generar el video
def generate_video():
    # Resolución del video
    width, height = 1920, 1080

    # Crear un video codificado con códec MJPEG
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_writer = cv2.VideoWriter('output.avi', fourcc, 25.0, (width, height))

    # Imagen de fondo
    background = np.zeros((height, width, 3), dtype=np.uint8)
    # Aquí puedes cargar la imagen que desees usar como fondo
    # background = cv2.imread('background_image.jpg')

    while True:
        # Obtener la hora actual
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)

        # Dibujar la hora en el centro de la imagen de fondo
        text_size, _ = cv2.getTextSize(current_time, cv2.FONT_HERSHEY_SIMPLEX, 2, 5)
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2
        cv2.putText(background, current_time, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

        # Escribir el fotograma en el video
        video_writer.write(background)

    # Liberar recursos
    video_writer.release()

# Función para transmitir el video por UDP utilizando ffmpeg
def transmit_video():
    udp_address = 'udp://127.0.0.1:1234'
    subprocess.run(['ffmpeg', '-re', '-i', 'output.avi', '-f', 'mpegts', udp_address])

if __name__ == "__main__":
    # Generar el video en segundo plano
    
    generate_process = subprocess.Popen(['python', '-c', 'import time; time.sleep(1); from udpvideo import generate_video; generate_video()'])

    # Transmitir el video por UDP
    time.sleep(3)
    transmit_video()

    # Esperar a que el proceso de generación del video termine
    generate_process.wait()