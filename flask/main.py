import subprocess
from flask import Flask, Response
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
from flask import Flask
from flask_cors import CORS
from flask_sse import sse

app = Flask(__name__)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')
CORS(app)

def generateImage(http_frame):
    # frame = np.zeros((480, 640, 3), np.uint8)
    # cv2.putText(frame, 'Nombre Equipo Local: ' + self.team_local.text(), (10, 50), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # cv2.putText(frame, 'Nombre Equipo Visitante: ' + self.team_visitor.text(), (10, 100), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # cv2.putText(frame, 'Puntos Equipo Local: ' + self.points_local.text(), (10, 150), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # cv2.putText(frame, 'Puntos Equipo Visitante: ' + self.points_visitor.text(), (10, 200), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # cv2.putText(frame, 'Tiempo: ' + self.current_time, (10, 250), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # filename = 'image.png'
    # cv2.imwrite(filename, frame)
    # self.image_counter += 1

# Crear una nueva imagen con el fondo verde

    # Definir los parámetros de la imagen
    http_frame = Image.frombytes('RGB', (640, 480), http_frame)
    http_frame = http_frame.convert("RGBA")
    color_fondo = (0, 0, 0)  # Color verde (RGB)
    resolucion = (1920, 1080)
    hora = str(datetime.now().strftime("%H:%M:%S"))
    print(hora)
    imagenes_textos = [
         {'tipo': 'imagen', 'posicion': (100, 100), 'contenido': 'cpbm.png'},
        {'tipo': 'imagen', 'posicion': (int(1920/2)-int(928/2), 1080-158-50), 'contenido': 'sb.png'},
        {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+85, 1080-158-40), 'contenido': {'texto': "CPBM", 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
        # {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+420, 1080-158-40), 'contenido': {'texto': self.team_visitor.text(), 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
        # {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+315, 1080-158-40), 'contenido': {'texto': self.points_local.text(), 'color': 'black', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
        # {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+650, 1080-158-40), 'contenido': {'texto': self.points_visitor.text(), 'color': 'black', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
        {'tipo': 'texto', 'posicion': ((1920/2)-(928/2), 1080-50-75), 'contenido': {'texto': hora, 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}}
]

    imagen = Image.new('RGBA', resolucion, color_fondo + (0,))
    imagen.paste(http_frame, (0,0), mask=http_frame)
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

    buffer = io.BytesIO()
    # imagen.save("test_frame.png")
    imagen.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def generate_frames():
    # Aquí deberías obtener frames de tu fuente de video en vivo
    # Puedes utilizar una librería como OpenCV para capturar video desde una cámara o una fuente en línea
    
    ffmpeg_command = [
    'ffmpeg',
    '-i', 'http://192.168.54.139:4747/video',
    '-f', 'image2pipe',  # Indicar que la salida será una secuencia de imágenes
    '-pix_fmt', 'rgb24',  # Formato de píxeles para mantener la transparencia
    '-vf', 'fps=30',  # Establecer la velocidad de fotogramas deseada (en este caso, 30 fps)
    '-vcodec', 'mjpeg',  # Codificar las imágenes en formato PNG
    '-'
]

# Iniciar el proceso de FFmpeg y redirigir la salida
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)
    while True:
        # Aquí debes generar los frames de video en vivo
        # Por ejemplo, utilizando OpenCV:
        # ret, frame = capturar_video.read()
        # Si utilizas una fuente de video en línea, puedes utilizar solicitudes HTTP para obtener los frames
        
        # Luego, convierte el frame en un formato adecuado, como JPEG
        # Por ejemplo, utilizando OpenCV:
        # ret, jpeg = cv2.imencode('.jpg', frame)
        http_frame = process.stdout.read(640*480 * 3)  # Ajustar el tamaño según la resolución de los frames
        # Devuelve el frame como bytes
        frame = generateImage(http_frame)
        # frame = frame.read()
        frame = frame.getvalue()
        # print(frame)
        try:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            pass
        
        # Por ahora, devolvemos un frame de prueba
        # yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + open('test_frame.png', 'rb').read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5001)