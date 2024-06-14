# Usa una imagen base oficial de Python
FROM python:3.9

RUN apt-get update \
    && apt-get install -y \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgl1-mesa-glx \
        build-essential

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos y los instala
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Instala uWSGI
RUN pip install uwsgi

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando para ejecutar uWSGI con tu aplicación
CMD ["uwsgi", "--socket", "0.0.0.0:5000", "--protocol", "http", "-w", "run:app", "--chdir", "/app", "--ssl-socket", "0.0.0.0:5000", "--ssl-cert", "cert.pem", "--ssl-key", "key.pem"]

