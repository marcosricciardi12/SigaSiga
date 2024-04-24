
from flask import Flask, jsonify, request, Response
from multiprocessing import Process, Manager
import time
import random
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
from flask_cors import CORS
app = Flask(__name__)
eventos = {}

def generate_frames(evento_id):
    # Aquí deberías obtener frames de tu fuente de video en vivo
    # Puedes utilizar una librería como OpenCV para capturar video desde una cámara o una fuente en línea
    
    while True:
        # Aquí debes generar los frames de video en vivo
        # Por ejemplo, utilizando OpenCV:
        # ret, frame = capturar_video.read()
        # Si utilizas una fuente de video en línea, puedes utilizar solicitudes HTTP para obtener los frames
        
        # Luego, convierte el frame en un formato adecuado, como JPEG
        # Por ejemplo, utilizando OpenCV:
        # ret, jpeg = cv2.imencode('.jpg', frame)
        
        # Devuelve el frame como bytes
        frame = open(str(evento_id)+ ".png", "rb")
        # print(frame)
        try:
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except:
            pass

def proceso_en_segundo_plano(evento_id, parametros, eventos_creados):
    while True:
        # print(eventos_creados)
        if evento_id not in eventos_creados:
            pass
            # break
        # Hacer alguna tarea asociada al evento con los parámetros actuales
        # print("\tPID EVENTO: " + str(os.getpid()))
        # print(f"\tTarea en segundo plano para evento {evento_id} con parámetros: {parametros}")
        with open(f'params_{evento_id}.txt', 'w') as f:
            f.write(str(parametros))

        color_fondo = (0, 0, 0)  # Color verde (RGB)
        resolucion = (1920, 1080)
        hora = str(datetime.now().strftime("%H:%M:%S"))
        # print(hora)
        imagenes_textos = [
            # {'tipo': 'imagen', 'posicion': (100, 100), 'contenido': 'cpbm.png'},
            {'tipo': 'imagen', 'posicion': (int(1920/2)-int(928/2), 1080-158-50), 'contenido': 'sb.png'},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+85, 1080-158-40), 'contenido': {'texto': parametros["nombre_local"], 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+420, 1080-158-40), 'contenido': {'texto': parametros["nombre_visita"], 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+315, 1080-158-40), 'contenido': {'texto': str(parametros["puntos_local"]), 'color': 'black', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': (int(1920/2)-int(928/2)+650, 1080-158-40), 'contenido': {'texto': str(parametros["puntos_visita"]), 'color': 'black', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}},
            {'tipo': 'texto', 'posicion': ((1920/2)-(928/2), 1080-50-75), 'contenido': {'texto': hora, 'color': 'white', 'fuente': 'arial.ttf', 'tamaño_fuente': 64}}
    ]

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

        buffer = io.BytesIO()
        imagen.save(f"{evento_id}.png")
        # imagen.save(buffer, format="PNG")
        # buffer.seek(0)
        # frame = generateImage()
        # frame = frame.read()
        # # print(frame)
        # try:
        #     yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        # except:
        #     pass
        time.sleep(0.1)

@app.route('/crear_evento/<evento_id>', methods=['POST'])
def crear_evento(evento_id):
    # time.sleep(10)
    if evento_id not in eventos:
        manager = Manager()
        parametros = manager.dict()
        parametros_nuevos = {"nombre_local": "default",
                             "puntos_local": 0,
                             "nombre_visita": "default",
                             "puntos_visita": 0,
                             }
        print("PID FLASK PADRE: " + str(os.getpid()))
        proceso = Process(target=proceso_en_segundo_plano, args=(evento_id, parametros, eventos))
        proceso.start()
        eventos[evento_id] = {"proceso": proceso, "parametros": parametros}
        eventos[evento_id]["parametros"].update(parametros_nuevos)
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
    if evento_id in eventos:
        puntos_local = eventos[evento_id]["parametros"]["puntos_local"] + 1
        parametros = {"puntos_local": puntos_local}
        eventos[evento_id]["parametros"].update(parametros)
        parametros = eventos[evento_id]["parametros"]
        return jsonify({"mensaje": f"Parámetros del evento {evento_id} modificados correctamente"},
                       {"Parametros": dict(parametros)}), 200
    else:
        return jsonify({"error": "El evento no existe"}), 404
    
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