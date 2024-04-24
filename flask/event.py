
from flask import Flask, jsonify, request
from multiprocessing import Process, Manager
import time
import random
import os
app = Flask(__name__)
eventos = {}

def proceso_en_segundo_plano(evento_id, parametros, eventos_creados):
    while True:
        print(eventos_creados)
        if evento_id not in eventos_creados:
            pass
            # break
        # Hacer alguna tarea asociada al evento con los parámetros actuales
        print("\tPID EVENTO: " + str(os.getpid()))
        print(f"\tTarea en segundo plano para evento {evento_id} con parámetros: {parametros}")
        with open(f'params_{evento_id}.txt', 'w') as f:
            f.write(str(parametros))
        time.sleep(random.randint(1, 5))

@app.route('/crear_evento/<evento_id>', methods=['POST'])
def crear_evento(evento_id):
    time.sleep(10)
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
    
if __name__ == '__main__':
    app.run(debug=False)