import os
import time
from main import redis

def countdown_timer(event_id):
    try:
        print(f'{event_id} timer started')
        while True and not int(redis.get(f'{event_id}-stop')):
            play_time = int(redis.get(f"{event_id}-scoreboard-play_time").decode("utf-8"))
            current_time = int(redis.get(f"{event_id}-scoreboard-time").decode("utf-8"))
            formatted_time = convertir_milisegundos_a_tiempo(current_time)
            redis.set(f"{event_id}-scoreboard-formatted_time", formatted_time)
            if play_time and current_time>0:
                time.sleep(0.01)
                current_time -= 10
                if current_time<=0: 
                    current_time=0
                    redis.set(f'{event_id}-scoreboard-play_time', int(False))
                redis.set(f"{event_id}-scoreboard-time", current_time)
                redis.set(f"{event_id}-scoreboard-formatted_time", formatted_time)
        os._exit(0)
    except:
        print("Timer closed")
        os._exit(0)

def convertir_milisegundos_a_tiempo(milisegundos):
    # Convertir milisegundos a segundos
    total_segundos = milisegundos / 1000
    
    # Obtener minutos
    minutos = int(total_segundos // 60)
    
    # Obtener segundos restantes
    segundos = int(total_segundos % 60)
    
    # Obtener décimas de segundo
    decimas = int((milisegundos % 1000) / 100)
    
    # Formatear el resultado como minutos:segundos:décimas
    tiempo_formateado = f"{minutos}:{segundos:02}.{decimas}"
    
    return tiempo_formateado