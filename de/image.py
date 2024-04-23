from PIL import Image, ImageDraw, ImageFont
import os
import time

# Tamaño de la imagen
width = 1920
height = 1080

# Ruta de la imagen a superponer en el centro
overlay_image_path = "cpbm.png"

# Función para generar la imagen con la hora del sistema y una imagen superpuesta
def generate_image_with_overlay():
    # Crear una nueva imagen en blanco
    image = Image.new("RGB", (width, height), color="green")

    # Abrir la imagen a superponer
    overlay_image = Image.open(overlay_image_path)

    # Calcular las coordenadas para colocar la imagen en el centro
    overlay_width, overlay_height = overlay_image.size
    x = (width - overlay_width) // 2
    y = (height - overlay_height) // 2

    # Superponer la imagen en el centro
    image.paste(overlay_image, (x, y))

    # Obtener la hora actual del sistema
    current_time = time.strftime("%H:%M:%S")

    # Crear un objeto ImageDraw
    draw = ImageDraw.Draw(image)

    # Especificar la fuente y el tamaño del texto
    font = ImageFont.truetype("arial.ttf", 100)

    # Obtener las dimensiones del texto
    # text_width, text_height = draw.textsize(current_time, font=font)

    # Calcular las coordenadas para centrar el texto
    text_x = (width - 1600) // 2
    text_y = (height - 0 ) // 2

    # Dibujar el texto en la imagen
    draw.text((text_x, text_y), current_time, fill="white", font=font)

    # Guardar la imagen generada
    image.save("image.png")

# # Generar la imagen con la hora del sistema y la imagen superpuesta
# generate_image_with_overlay()

if __name__ == "__main__":
    while True:
        generate_image_with_overlay()
        time.sleep(0.1)  # Espera 1 segundo antes de generar la próxima imagen