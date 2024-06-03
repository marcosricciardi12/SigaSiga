
import base64
import cv2
import os
import time
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from main.services.scoreboard_services import get_scoreboard
import ast
import io

def generate_final_video(redis_db, event_id):
    try:
        video_source_index = int(redis_db.get(f'{event_id}-selected_socket_video_source'))
        video_list = redis_db.get(f'{event_id}-socket_video_sources')
        bytes_video_list = video_list.decode('utf-8')
        video_list = ast.literal_eval(bytes_video_list)
        key_user_video_source = str(video_list[video_source_index])
        key_video_source = f'{event_id}-socket_video_sources-{key_user_video_source}'
        print("hola", key_video_source)
        scoreboard_image = Image.open('sb.png').convert('RGBA')
        alfa = 0
        scoreboard = get_scoreboard(event_id)
        # capture = capture_list[0]
        print(os.getpid(), event_id, scoreboard)
        while not int(redis_db.get(f'{event_id}-stop')):
            # start_time = time.time()
            if int(redis_db.get(f'{event_id}-interrupt_flag')):
                redis_db.set(f'{event_id}-interrupt_flag', int(False))
                video_source_index = int(redis_db.get(f'{event_id}-selected_socket_video_source'))
                video_list = redis_db.get(f'{event_id}-socket_video_sources')
                bytes_video_list = video_list.decode('utf-8')
                video_list = ast.literal_eval(bytes_video_list)
                key_user_video_source = str(video_list[video_source_index])
                key_video_source = f'{event_id}-socket_video_sources-{key_user_video_source}'
                print(video_source_index)

            # frame_bytes = redis_db.get(key_video_source)
            # # if frame_bytes:
            # #     # Convertir los bytes del frame a formato de imagen
            # nparr = np.frombuffer(frame_bytes, np.uint8)
            # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            frame = get_frame_from_redis(key_video_source, redis_db)
            scoreboard = get_scoreboard(event_id)
            # scoreboard_image.putalpha(int(alfa))
            # if alfa >=255:
            #     alfa = 0
            # alfa += 1
            
            # Convertir el frame de OpenCV a Pillow
            pillow_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pillow_frame = Image.fromarray(pillow_frame)
            y_factor = 1080/pillow_frame.height
            height_frame = 1080
            width_frame = int(pillow_frame.width * y_factor)
            pillow_frame = pillow_frame.resize((width_frame, height_frame))
            pillow_frame = pillow_frame.convert("RGBA")
            # Crear un lienzo de 1920x1080 y agregar el frame en el centro
            canvas = Image.new('RGBA', (1920, 1080), color='black')
            draw = ImageDraw.Draw(canvas)
            
            
            canvas.paste(pillow_frame, ((1920 - pillow_frame.width) // 2, (1080 - pillow_frame.height) // 2))
            
            # Agregar la imagen con transparencia en el centro inferior cercano al borde
            if video_source_index!=0:
                canvas.paste(scoreboard_image, ((1920 - scoreboard_image.width) // 2, 1080 - scoreboard_image.height), mask=scoreboard_image)
                hora = str(datetime.now().strftime("%H:%M:%S"))
                draw.text((1920-200,1080-100), hora , fill="white", font=ImageFont.truetype("arial.ttf", 32))
                draw.text((600,930), scoreboard["local_team_short"] , fill="white", font=ImageFont.truetype("arial.ttf", 64))
                draw.text((785,930), scoreboard["local_points"] , fill="black", font=ImageFont.truetype("arial.ttf", 64))
                draw.text((939,930), scoreboard["visitor_team_short"] , fill="white", font=ImageFont.truetype("arial.ttf", 64))
                draw.text((1124,930), scoreboard["visitor_points"] , fill="black", font=ImageFont.truetype("arial.ttf", 64))
            else:
                hora = str(datetime.now().strftime("%H:%M:%S"))
                draw.text((1920-200,1080-100), hora , fill="white", font=ImageFont.truetype("arial.ttf", 32))

            canvas = canvas.convert('RGB')
            # canvas.save("img.jpeg")
            # Convertir el lienzo a bytes
            # frame_bytes = canvas.tobytes("JPEG")
            buffer = io.BytesIO()
            # imagen.save("test_frame.png")
            canvas.save(buffer, format="JPEG")
            buffer.seek(0)
            video_frame = buffer.read()
            redis_db.set(f'{event_id}-video_frame', video_frame)
        
        redis_db.delete(f'{event_id}-video_frame')
    except Exception as e:
        print("Generacion de video terminada.(Excepcion)", e)
        redis_db.delete(f'{event_id}-video_frame')
    os._exit(0)

def get_frame_from_redis(key, redis):
    # Obtener el frame almacenado en Redis
    encoded_frame = redis.get(key)
    if encoded_frame is None:
        print("No frame found in Redis for the given key.")
        return None

    # Decodificar el frame de base64
    webp_frame = base64.b64decode(encoded_frame)

    # Convertir los bytes del frame WebP a una matriz de imagen que OpenCV pueda usar
    image_array = np.frombuffer(webp_frame, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image