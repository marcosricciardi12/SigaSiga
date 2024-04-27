import time
from flask import Flask, Response
import cv2
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime
app = Flask(__name__)

def generate_frames():
    # Captura de la fuente de video con OpenCV
    capture = cv2.VideoCapture('http://192.168.54.139:4747/video')
    transparent_image = Image.open('sb.png').convert('RGBA')
    alfa = 0
    while True:
        ret, frame = capture.read()
        # transparent_image.putalpha(int(alfa))
        # if alfa >=255:
        #     alfa = 0
        # alfa += 1
        if not ret:
            continue
        
        # Convertir el frame de OpenCV a Pillow
        pillow_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pillow_frame = Image.fromarray(pillow_frame)
        pillow_frame = pillow_frame.resize((1440, 1080))
        pillow_frame = pillow_frame.convert("RGBA")
        # Crear un lienzo de 1920x1080 y agregar el frame en el centro
        canvas = Image.new('RGBA', (1920, 1080), color='black')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(pillow_frame, ((1920 - pillow_frame.width) // 2, (1080 - pillow_frame.height) // 2))
        
        # Agregar la imagen con transparencia en el centro inferior cercano al borde
        canvas.paste(transparent_image, ((1920 - transparent_image.width) // 2, 1080 - transparent_image.height), mask=transparent_image)
        hora = str(datetime.now().strftime("%H:%M:%S"))
        draw.text((0,0), hora , fill="white", font=ImageFont.truetype("arial.ttf", 64))
        canvas = canvas.convert('RGB')
        canvas.save("img.jpeg")
        # Convertir el lienzo a bytes
        # frame_bytes = canvas.tobytes("JPEG")
        buffer = io.BytesIO()
        # imagen.save("test_frame.png")
        canvas.save(buffer, format="JPEG")
        buffer.seek(0)
        # Generar el frame para la fuente de video HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.read() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
