import subprocess
import time

# Ruta de la imagen de entrada
input_image = "image.png"

# Ruta del dispositivo de video virtual
video_device = "/dev/video2"

# Intervalo de tiempo en segundos para recargar la imagen
interval = 0.033

# Función para capturar la imagen y transmitirla como video
def capture_and_transmit():
    # Comando ffmpeg para capturar la imagen y transmitirla como video
    command = [
        "ffmpeg",
        "-loop", "1",
        "-i", input_image,
        "-vf", "format=yuv420p",
        "-f", "v4l2",
        video_device
    ]
    # Ejecutar el comando ffmpeg
    # command = [
    #     "ffmpeg",
    #     "-loop", "1",
    #     "-i", "image.png",
    #     "-c:v", "libx264",
    #     "-tune", "stillimage",
    #     "-pix_fmt", "yuv420p",
    #     "-f", "mpegts",
    #     "udp://127.0.0.1:1234"
    # ]
    subprocess.run(command)


# Bucle infinito para capturar y transmitir la imagen cada cierto tiempo
while True:
    # Capturar y transmitir la imagen
    capture_and_transmit()

    # Esperar el intervalo de tiempo especificado
    time.sleep(interval)