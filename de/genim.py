from PIL import Image, ImageDraw, ImageFont

def crear_imagen(fondo_color, resolucion, imagenes_textos):
    # Crear una nueva imagen con el fondo verde
    imagen = Image.new('RGBA', resolucion, color_fondo + (0,))
    draw = ImageDraw.Draw(imagen)

    # Añadir imágenes y texto sobre la imagen base
    for item in imagenes_textos:
        tipo = item['tipo']
        posicion = item['posicion']
        contenido = item['contenido']

        if tipo == 'imagen':
            imagen_path = contenido
            imagen_overlay = Image.open(imagen_path).convert('RGBA')
            imagen.paste(imagen_overlay, posicion, mask=imagen_overlay)
        elif tipo == 'texto':
            texto = contenido['texto']
            color = contenido.get('color', 'black')
            fuente_path = contenido.get('fuente', None)
            tamaño_fuente = contenido.get('tamaño_fuente', 34)

            if fuente_path:
                fuente = ImageFont.truetype(fuente_path, tamaño_fuente)
            else:
                fuente = ImageFont.load_default()

            draw.text(posicion, texto, fill=color, font=fuente)

    return imagen

# Definir los parámetros de la imagen
color_fondo = (0, 255, 0)  # Color verde (RGB)
resolucion = (1920, 1080)
imagenes_textos = [
    {'tipo': 'imagen', 'posicion': (100, 100), 'contenido': 'cpbm.png'},
    {'tipo': 'imagen', 'posicion': (500, 500), 'contenido': 'sb.png'},
    {'tipo': 'texto', 'posicion': (200, 200), 'contenido': {'texto': 'Texto de ejemplo', 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}}
]

# Crear la imagen
imagen = crear_imagen(color_fondo, resolucion, imagenes_textos)
# imagen.show()  # Mostrar la imagen generada
imagen.save('imagen_generada.png')  # Guardar la imagen generada
