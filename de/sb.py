import cv2
import numpy as np

# Dimensiones del video
width, height = 1920, 1080
# FPS (cuadros por segundo)
fps = 30
# Duración del video en segundos
duration = 10
# Cargar la imagen
image = cv2.imread('sb.png', cv2.IMREAD_UNCHANGED)
image_height, image_width = image.shape[:2]

# Color verde para el fondo
green_color = (0, 255, 0)

# Codec de video (MP4V)
codec = cv2.VideoWriter_fourcc(*'mp4v')
# Nombre del archivo de video de salida
output_file = 'video_con_imagen.mp4'

# Crear un objeto VideoWriter
out = cv2.VideoWriter(output_file, codec, fps, (width, height))

# Calcular la posición para colocar la imagen en el centro
start_x = (width - image_width) // 2
start_y = (height - image_height) // 2

# Crear los cuadros del video
for i in range(duration * fps):
    # Crear un cuadro con fondo verde
    frame = np.ones((height, width, 3), dtype=np.uint8) * green_color
    # Superponer la imagen en el centro
    frame[start_y:start_y + image_height, start_x:start_x + image_width] = image[:, :, :3]
    # Convertir la matriz de imagen a tipo de datos CV_8U
    frame = np.uint8(frame)
    # Escribir el cuadro en el video
    out.write(frame)

# Liberar el objeto VideoWriter
out.release()
