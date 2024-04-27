from flask import Flask, Response
import cv2
from PIL import Image, ImageDraw
import io
app = Flask(__name__)

def generate_frames():
    # Captura de la fuente de video con OpenCV
    # cap = cv2.VideoCapture('http://192.168.54.139:4747/video')
    transparent_image = Image.open('sb.png')
    while True:
        # ret, frame = cap.read()
        # if not ret:
            # continue
        # cv2.imshow('Video', frame)
        
        # Convertir el frame de OpenCV a Pillow
        # pillow_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # pillow_frame = Image.fromarray(pillow_frame)
        
        # Crear un lienzo de 1920x1080 y agregar el frame en el centro
        canvas = Image.new('RGB', (1920, 1080), color='green')
        # canvas.paste(pillow_frame, ((1920 - pillow_frame.width) // 2, (1080 - pillow_frame.height) // 2))
        
        # Agregar la imagen con transparencia en el centro inferior cercano al borde
        canvas.paste(transparent_image, ((1920 - transparent_image.width) // 2, 1080 - transparent_image.height))
        
        # Convertir el lienzo a bytes
        buffer = io.BytesIO()
        # imagen.save("test_frame.png")
        canvas.save(buffer, format="JPEG")
        buffer.seek(0)
        # Generar el frame para la fuente de video HTTP
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.read() + b'\r\n')
    cap.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True, port=8000)