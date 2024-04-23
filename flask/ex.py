from flask import Flask, Response
import requests
import random

app = Flask(__name__)

def fetch_frames():
    # URL de la fuente de video HTTP
    video_url = 'http://localhost:5000/video_feed'
    
    # Haces una solicitud GET para obtener las imágenes de la fuente HTTP
    response = requests.get(video_url, stream=True)
    
    # Iteras sobre los datos recibidos y los transmites como chunks
    frame_counter = random.randint(0, 100000000)

    for chunk in response.iter_content(chunk_size=1024):
        # Escribe el chunk en un archivo PNG en el disco
        with open(f'frame_{frame_counter}.png', 'ab') as f:
            f.write(chunk)
        # Incrementa el contador de frames
        # Devuelve el chunk como parte de la respuesta
        yield chunk

@app.route('/video_feed')
def video_feed():
    # Retorna la respuesta de streaming con los frames capturados
    return Response(fetch_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=5005)