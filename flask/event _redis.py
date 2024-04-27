
from flask import Flask, jsonify, request, Response
from multiprocessing import Process, Manager
import subprocess
import time
import random
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
from flask_cors import CORS
from redis import Redis
import json
import cv2

app = Flask(__name__)
app.config['REDIS_URL'] = 'redis://localhost:6379/0'  # Cambia esto según la configuración de tu servidor Redis
redis = Redis.from_url(app.config['REDIS_URL'])
eventos = {}

def generate_frames(evento_id):
    # Aquí deberías obtener frames de tu fuente de video en vivo
    # Puedes utilizar una librería como OpenCV para capturar video desde una cámara o una fuente en línea
    
    while True:
        read_frame = redis.get(evento_id + "_frame")
        if read_frame:
            frame = read_frame
        # print(frame)
        try:
            yield (b'--frame\r\n' b'Content-Type: image/png\r\n\r\n' + frame + b'\r\n')
        except:
            pass

def proceso_en_segundo_plano(evento_id, redis):

    # accumulated_frames = []
    # batch_size = 300

    # ffmpeg_cmd = [
    #     'ffmpeg',
    #     '-y',  # Sobrescribir el archivo de salida si ya existe
    #     '-loop', '1',  # Repetir el frame
    #     '-framerate', f'{1/0.3:.2f}',  # FPS inverso de la duración del frame
    #     '-i', '-',  # La entrada es la tubería de imágenes (stdin)
    #     '-c:v', 'libx264',  # Codificador de video: libx264
    #     '-preset', 'ultrafast',  # Preset para la velocidad de codificación
    #     '-tune', 'zerolatency',  # Ajuste para la baja latencia
    #     '-f', 'flv',  # Formato de salida: FLV (para RTMP)
    #     "rtmp://localhost/live/stream"  # URL del servidor RTMP
    # ]
    # ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # video_url = 'http://192.168.54.139:4747/video'
    # cap = cv2.VideoCapture(video_url)
    # if not cap.isOpened():
    #     print("Error: No se pudo abrir la captura de video.")
    #     exit()

    # ffmpeg_cmd_http = [
    #     'ffmpeg',
    #     '-i', 'http://192.168.54.139:4747/video',  # Reemplaza con tu fuente de video HTTP
    #     '-f', 'image2pipe',
    #     '-vf', 'fps=30',  # Captura un fotograma por segundo
    #     '-pix_fmt', 'rgb24',
    #     '-vcodec', 'rawvideo',
    #     '-',
    # ]
    # process_http = subprocess.Popen(ffmpeg_cmd_http, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    process = subprocess.Popen([
        'ffmpeg',
        '-f', 'image2pipe',
        '-i', 'pipe:',
        '-f', 'v4l2',
        '-vcodec', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-video_size', '1920x1080',
        "/dev/video2"
    ], stdin=subprocess.PIPE)

    while True:
        # ret, frame = cap.read()
        # if ret:
        #     # Convierte el fotograma a una imagen en Pillow
        #     img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA))
        # frame_http = process_http.stdout.read(640 * 480 * 3)
        parametros = {"nombre_local": "default",
                             "puntos_local": 0,
                             "nombre_visita": "default",
                             "puntos_visita": 0,
                             "frame": "",
        }
        for key in parametros:
            parametros[key] = redis.get(str(evento_id) + "_" + key)

        with open(f'params_{evento_id}.txt', 'w') as f:
            f.write(str(parametros))

        color_fondo = (0, 255, 0)  # Color verde (RGB)
        resolucion = (1920, 1080)
        hora = str(datetime.now().strftime("%H:%M:%S"))
        # print(hora)
        imagenes_textos = [
            # {'tipo': 'imagen', 'posicion': (100, 100), 'contenido': 'cpbm.png'},
            {'tipo': 'imagen', 'posicion': (int(1920/2)-int(928/2), 1080-158-50), 'contenido': 'sb.png'},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+85, 1080-158-40), 'contenido': {'texto': str(parametros["nombre_local"].decode()), 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+420, 1080-158-40), 'contenido': {'texto': str(parametros["nombre_visita"].decode()), 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+315, 1080-158-40), 'contenido': {'texto': str(parametros["puntos_local"].decode()), 'color': 'black', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+650, 1080-158-40), 'contenido': {'texto': str(parametros["puntos_visita"].decode()), 'color': 'black', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': ((1920/2)-(928/2), 1080-50-75), 'contenido': {'texto': hora, 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}}
    ]

        imagen = Image.new('RGBA', resolucion, color_fondo + (0,))
        draw = ImageDraw.Draw(imagen)

        # if frame_http:
        #     imagen_overlay = Image.frombytes('RGB', (640, 480), frame_http)
        #     imagen_overlay = imagen_overlay.convert("RGBA")
        #     imagen.paste(imagen_overlay, (0,0), mask=imagen_overlay)
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
        imagen = imagen.convert("RGB")
        imagen.save(buffer, format="JPEG")
        buffer.seek(0)

        parametros["frame"] = buffer.read()
        process.stdin.write(parametros["frame"])
        process.stdin.flush()


        time.sleep(1 / 30)
        redis.set(str(evento_id) + "_frame", parametros["frame"])

        # accumulated_frames.append(parametros["frame"])
        # if len(accumulated_frames) >= batch_size:
        #     batch_frame = b''.join(accumulated_frames)
        #     ffmpeg_process.stdin.write(batch_frame)
        #     accumulated_frames.clear()  # Limpiar la lista de frames acumulados
        # time.sleep(0.1)

@app.route('/crear_evento/<evento_id>', methods=['POST'])
def crear_evento(evento_id):
    # time.sleep(10)
    if evento_id not in eventos:
        parametros_nuevos = {"nombre_local": "default",
                             "puntos_local": 0,
                             "nombre_visita": "default",
                             "puntos_visita": 0,
                             "frame": "",
                             }
        for key in parametros_nuevos:
            redis.set(str(evento_id) + "_" + key, parametros_nuevos[key])
        # print(redis.get(evento_id))
        print("PID FLASK PADRE: " + str(os.getpid()))
        proceso = Process(target=proceso_en_segundo_plano, args=(evento_id, redis))
        proceso.start()
        return jsonify({"mensaje": f"Evento {evento_id} creado correctamente"}), 200
    else:
        return jsonify({"error": "El evento ya existe"}), 400

@app.route('/detener_evento/<evento_id>', methods=['POST'])
def detener_evento(evento_id):
    if evento_id in eventos:
        proceso = eventos[evento_id]["proceso"]
        proceso.terminate()  # Detener el proceso
        del eventos[evento_id]
        return jsonify({"mensaje": f"Evento {evento_id} detenido correctamente"}), 200
    else:
        return jsonify({"error": "El evento no existe"}), 404

@app.route('/modificar_parametros/<evento_id>', methods=['POST'])
def modificar_parametros(evento_id):
    if evento_id in eventos:
        parametros = request.json
        eventos[evento_id]["parametros"].update(parametros)
        return jsonify({"mensaje": f"Parámetros del evento {evento_id} modificados correctamente"}), 200
    else:
        return jsonify({"error": "El evento no existe"}), 404
    
@app.route('/sum_local/<evento_id>', methods=['POST'])
def sum_local(evento_id):
    # if evento_id in eventos:
        puntos_local = redis.get(evento_id +"_puntos_local")
        puntos_local = int(puntos_local.decode())
        puntos_local += 1
        redis.set(evento_id +"_puntos_local", puntos_local)
        return jsonify({"mensaje": f"Parámetros del evento {evento_id} modificados correctamente"},
                       {"Parametros": str(puntos_local)}), 200
    # else:
    #     return jsonify({"error": "El evento no existe"}), 404
    
@app.route('/rest_local/<evento_id>', methods=['POST'])
def rest_local(evento_id):
    if evento_id in eventos:
        puntos_local = eventos[evento_id]["parametros"]["puntos_local"] - 1
        parametros = {"puntos_local": puntos_local}
        eventos[evento_id]["parametros"].update(parametros)
        parametros = eventos[evento_id]["parametros"]
        return jsonify({"mensaje": f"Parámetros del evento {evento_id} modificados correctamente"},
                       {"Parametros": dict(parametros)}), 200
    else:
        return jsonify({"error": "El evento no existe"}), 404

@app.route('/obtener_parametros/<evento_id>', methods=['GET'])
def obtener_parametros(evento_id):
    if evento_id in eventos:
        parametros = eventos[evento_id]["parametros"]
        return jsonify({"parametros": dict(parametros)}), 200
    else:
        return jsonify({"error": "El evento no existe"}), 404

@app.route('/video_feed/<evento_id>', methods=['GET'])
def video_feed(evento_id):
    return Response(generate_frames(evento_id), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=False)