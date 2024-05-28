import base64
import time
from flask_socketio import SocketIO
from flask import request
from main import redis
socketio = SocketIO()

# @socketio.on('connect')
# def handle_connect():
#     client_id = request.sid
#     print('Conexión establecida con:', client_id)

leftover_bytes = b''

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    print('Conexión establecida con: ' , client_id)

@socketio.on('send_parameters')
def handle_parameters(data):
    video_source_key = data.get('video_source_key')
    client_id = request.sid
    print('video_source_key 1:', video_source_key)
    redis.set(client_id, video_source_key)

# @socketio.on('send_frame_from_client')
# def handle_frame_from_client(data):
#     # print('Hora del cliente:', data['client_time'])
#     try:
#         client_id = request.sid
#         # video_source_key = redis.get(client_id)
#         video_source_key = "video_frame"
#         frame_bytes = data['video_frame']
#         # print(frame_bytes[:20])
#         redis.set(video_source_key, frame_bytes)
#     except:
#         pass

@socketio.on('send_frame_from_client')
def handle_frame_from_client(data):
    global leftover_bytes

    try:
        client_id = request.sid
        video_source_key = "video_frame"

        # Combinar bytes sobrantes con los nuevos datos recibidos
        frame_bytes = leftover_bytes + data['video_frame']
        # print(data['video_frame'][:20])
        # Buscar el marcador de inicio y fin de imagen JPEG
        start_marker = b'\xff\xd8'  # Marcador de inicio de imagen JPEG
        end_marker = b'\xff\xd9'    # Marcador de fin de imagen JPEG
        
        start_index = frame_bytes.find(start_marker)
        end_index = frame_bytes.find(end_marker)
        
        # Si se encontraron ambos marcadores, se tiene un frame JPEG completo
        if start_index != -1 and end_index != -1:
            # Extraer el frame JPEG completo
            jpeg_frame = frame_bytes[start_index:end_index + 2]
            
            # Guardar bytes sobrantes para la próxima recepción de datos
            leftover_bytes = frame_bytes[end_index + 2:]
            
            # Escribir el frame en Redis o realizar otras operaciones necesarias
            redis.set(video_source_key, jpeg_frame)
            
            print("Frame guardado correctamente")
        else:
            # Si no se encontraron ambos marcadores, guardar bytes sobrantes para la próxima recepción
            leftover_bytes = frame_bytes

    except Exception as e:
        print("Error al procesar el frame:", e)


@socketio.on('frame2')
def handle_frame(frame):
    # Procesar el frame recibido (guardar en disco, analizar, etc.)
    video_source_key = "video_frame"
    print(frame[:30])
    print(base64.b64decode(frame)[:30])
    redis.set(video_source_key, frame)
    # print('Frame recibido:', frame)

# @socketio.on('frame')
# def handle_frame_from_client(data):
#     global leftover_bytes
#     try:
#         client_id = request.sid
#         print(data[:27])
#         video_source_key = "video_frame"
#         frame_data = data.split(',')[1]  # Remove the 'data:image/jpeg;base64,' part
#         frame_data_bytes = base64.b64decode(frame_data)
#         # Combinar bytes sobrantes con los nuevos datos recibidos
#         frame_bytes = leftover_bytes + frame_data_bytes
#         # print(data['video_frame'][:20])
#         # Buscar el marcador de inicio y fin de imagen JPEG
#         start_marker = b'\xff\xd8'  # Marcador de inicio de imagen JPEG
#         end_marker = b'\xff\xd9'    # Marcador de fin de imagen JPEG
        
#         start_index = frame_bytes.find(start_marker)
#         end_index = frame_bytes.find(end_marker)
        
#         # Si se encontraron ambos marcadores, se tiene un frame JPEG completo
#         if start_index != -1 and end_index != -1:
#             # Extraer el frame JPEG completo
#             jpeg_frame = frame_bytes[start_index:end_index + 2]
            
#             # Guardar bytes sobrantes para la próxima recepción de datos
#             leftover_bytes = frame_bytes[end_index + 2:]
            
#             # Escribir el frame en Redis o realizar otras operaciones necesarias
#             redis.set(video_source_key, base64.b64encode(jpeg_frame))
            
#             print("Frame guardado correctamente")
#         else:
#             # Si no se encontraron ambos marcadores, guardar bytes sobrantes para la próxima recepción
#             leftover_bytes = frame_bytes

#     except Exception as e:
#         print("Error al procesar el frame:", e)

@socketio.on('frame')
def handle_frame_from_client(data):
    global leftover_bytes
    try:
        # Decodificar el frame base64 recibido
        frame_data_bytes = base64.b64decode(data)
        # Combinar bytes sobrantes con los nuevos datos recibidos
        frame_bytes = leftover_bytes + frame_data_bytes

        # Marcador de inicio de imagen WebP
        start_marker = b'RIFF'
        next_start_index = 0

        while True:
            start_index = frame_bytes.find(start_marker, next_start_index)
            if start_index == -1:
                # No se encontró el próximo marcador de inicio, guardar bytes sobrantes
                leftover_bytes = frame_bytes
                break

            # Buscar el próximo marcador de inicio
            next_start_index = frame_bytes.find(start_marker, start_index + len(start_marker))
            if next_start_index == -1:
                # No se encontró el próximo marcador, guardar bytes sobrantes
                leftover_bytes = frame_bytes[start_index:]
                break

            # Extraer el frame WebP completo
            webp_frame = frame_bytes[start_index:next_start_index]

            # Guardar el frame WebP en Redis
            redis_key = "video_frame"
            redis.set(redis_key, base64.b64encode(webp_frame))

            # print("Frame guardado correctamente")

    except Exception as e:
        print("Error al procesar el frame:", e)