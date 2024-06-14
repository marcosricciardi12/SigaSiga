import ast
import base64
import time
from flask_socketio import SocketIO, disconnect
from flask import jsonify, request
from main import redis
import jwt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

socketio = SocketIO()

leftover_bytes = b''

# @socketio.on('connect')
# def handle_connect():
#     client_id = request.sid
#     print('Conexión establecida con: ' , client_id)

@socketio.on('connect')
def connect():
    token = request.args.get('token')
    client_id = request.sid
    try:
        jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
        print('Usuario conectado')
        token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
        user_identity = token_decode['sub']['user_id']
        event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')
        video_source_key = f'{event_id}-socket_video_sources-{user_identity}'
        
        print("Client connected")

    except jwt.ExpiredSignatureError:
        print('Token expirado')
        return False
    except jwt.InvalidTokenError:
        print('Token inválido')
        return False

@socketio.on('disconnect')
def handle_disconnect():
    token = request.args.get('token')
    client_id = request.sid
    try:
        jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
        token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
        user_identity = token_decode['sub']['user_id']
        event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')
        print('Client disconnected!!!')

    except jwt.ExpiredSignatureError:
        print('Token expirado')
        return False
    except jwt.InvalidTokenError:
        print('Token inválido')
        return False
    

@socketio.on('disconnect_request')
def handle_disconnect_request():
    disconnect()

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
    client_id = request.sid
    token = request.args.get('token')
    token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
    user_identity = token_decode['sub']['user_id']
    event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')
    video_source_key = f'{event_id}-socket_video_sources-{client_id}'

    key_leftover_bytes = client_id + '-' + event_id
    leftover_bytes  = redis.get(key_leftover_bytes)
    # print(video_source_key)
    try:
        pass
        # print('Usuario valido: ', user_identity, ' Evento ID: ', event_id)
        
    except jwt.ExpiredSignatureError:
        print('Token expirado')
        return False
    except jwt.InvalidTokenError:
        print('Token inválido')
        return False
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
                redis.set(key_leftover_bytes, leftover_bytes)
                break

            # Buscar el próximo marcador de inicio
            next_start_index = frame_bytes.find(start_marker, start_index + len(start_marker))
            if next_start_index == -1:
                # No se encontró el próximo marcador, guardar bytes sobrantes
                leftover_bytes = frame_bytes[start_index:]
                redis.set(key_leftover_bytes, leftover_bytes)
                break

            # Extraer el frame WebP completo
            webp_frame = frame_bytes[start_index:next_start_index]

            # Guardar el frame WebP en Redis
            # redis.set(video_source_key, base64.b64encode(webp_frame))
            redis.set(video_source_key, webp_frame)
            # print(video_source_key)
            # print("Frame guardado correctamente")

    except Exception as e:
        print("Error al procesar el frame:", e)


@socketio.on('add_video_socket')
def handle_add_socket_from_client():
    client_id = request.sid
    token = request.args.get('token')
    token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
    user_identity = token_decode['sub']['user_id']
    event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')

    key_leftover_bytes = client_id + '-' + event_id
    leftover_bytes = b''
    redis.set(key_leftover_bytes, leftover_bytes)
    
    video_source_key = f'{event_id}-socket_video_sources-{client_id}'

    video_list = redis.get(f'{event_id}-socket_video_sources')
    if video_list:
        bytes_video_list = video_list.decode('utf-8')
        video_list = ast.literal_eval(bytes_video_list)
    else:
        video_list = []
    video_list.append(client_id)
    redis.set(f'{event_id}-socket_video_sources', str(video_list))

    print("Video socket added: ", video_source_key)
    video_list_to_send = get_event_video_sources_list(event_id, video_list)
    director_room_notify(event_id, video_list_to_send)
    return {"video_source_list": video_list}


@socketio.on('del_video_socket')
def handle_del_socket_from_client():
    client_id = request.sid
    token = request.args.get('token')
    token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
    user_identity = token_decode['sub']['user_id']
    event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')
    video_source_key = f'{event_id}-socket_video_sources-{client_id}'

    video_list = redis.get(f'{event_id}-socket_video_sources')
    print("hay que eliminar video de la siguiente lista: ")
    print(video_list)
    if video_list:
        bytes_video_list = video_list.decode('utf-8')
        video_list = ast.literal_eval(bytes_video_list)
        video_source_index =  int(video_list.index(client_id))
        print("video a eliminar indice: ", video_source_index)
        video_selected_index = int(redis.get(f'{event_id}-selected_socket_video_source'))
        print("video seleccionado indice: ", video_selected_index)
        if video_source_index == video_selected_index:
            redis.set(f'{event_id}-interrupt_flag', int(True))
            redis.set(f'{event_id}-selected_socket_video_source', int(0))
        print("cliente a remover: ",  client_id)
        video_list.remove(client_id)
        redis.delete(video_source_key)
        redis.set(f'{event_id}-socket_video_sources', str(video_list))
    else:
        video_list = []
    
    video_list_to_send = get_event_video_sources_list(event_id, video_list)
    director_room_notify(event_id, video_list_to_send)
    return {"video_source_list": video_list}


@socketio.on('director_room_join')
def handle_director_room_join():
    print("Se ha unido alguien a la sala de director")
    client_id = request.sid
    token = request.args.get('token')
    token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
    user_identity = token_decode['sub']['user_id']
    event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')

    director_room_list = redis.get(f'{event_id}-director_room')
    if director_room_list:
        bytes_director_room_list = director_room_list.decode('utf-8')
        director_room_list = ast.literal_eval(bytes_director_room_list)
    else:
        director_room_list = []
    director_room_list.append(client_id)
    print(director_room_list)
    redis.set(f'{event_id}-director_room', str(director_room_list))


@socketio.on('director_room_leave')
def handle_director_room_leave():
    client_id = request.sid
    token = request.args.get('token')
    token_decode = jwt.decode(token, "asfgakdfjsdkfhkas", algorithms=["HS256"])
    user_identity = token_decode['sub']['user_id']
    event_id = (redis.get(f"user-{user_identity}-id_event")).decode('utf-8')

    director_room_list = redis.get(f'{event_id}-director_room')
    if director_room_list:
        bytes_director_room_list = director_room_list.decode('utf-8')
        director_room_list = ast.literal_eval(bytes_director_room_list)
    else:
        director_room_list = []
    director_room_list.remove(client_id)
    redis.set(f'{event_id}-director_room', str(director_room_list))



def director_room_notify(event_id, video_list_to_send):
    print(event_id)
    director_room_list = redis.get(f'{event_id}-director_room')
    print("Hay que notificar a: ", director_room_list)
    if director_room_list:
        bytes_director_room_list = director_room_list.decode('utf-8')
        director_room_list = ast.literal_eval(bytes_director_room_list)
    else:
        director_room_list = []
    print("Hay que notificar a: ", director_room_list)
    for client_id in director_room_list:
         print("\n\nnotify to: ", client_id)
         print(video_list_to_send)
         socketio.emit('directors_notification', {"video_list":(video_list_to_send)}, to=client_id)

def get_event_video_sources_list(event_id, video_list):
    selected_video_source = int(redis.get(f"{event_id}-selected_socket_video_source"))
    list_video_source = []
    for video_source in video_list:
        title = video_source
        if title == video_list[selected_video_source]:
            status = True
        else:
            status = False
        list_video_source.append({"title": title, "active": status})
    return str(list_video_source)