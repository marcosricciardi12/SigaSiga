import cv2

# Abrir el dispositivo de video virtual en modo de escritura
video_writer = cv2.VideoWriter('/dev/video2', cv2.CAP_V4L2, 30, (1920, 180))

# Ruta al archivo de video
video_file = '/home/marcos/video_grabado.mp4'

# Abrir el archivo de video
cap = cv2.VideoCapture(video_file)

while True:
    ret, frame = cap.read()  # Leer un frame del archivo de video
    if ret:
        video_writer.write(frame)  # Escribir el frame en el dispositivo de video virtual
    else:
        break

# Liberar los recursos
cap.release()