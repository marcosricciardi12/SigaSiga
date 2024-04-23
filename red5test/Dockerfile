# Utilizar la imagen base de Ubuntu
FROM ubuntu:22.04

# Actualizar el índice de paquetes e instalar dependencias necesarias
RUN apt-get update && \
    apt-get install -y git openjdk-11-jdk

# Clonar el repositorio de instalación de Red5Pro
RUN git clone https://github.com/red5pro/red5pro-installer.git

# Entrar en el directorio del repositorio clonado
WORKDIR /red5pro-installer

# Cambiar los permisos de los archivos .sh
RUN chmod +x *.sh

# Ejecutar el script de instalación de Red5Pro
# RUN echo "1" | echo "1" | ./red5proInstaller.sh

# Exponer el puerto de Red5Pro que desees utilizar (normalmente el puerto 5080)
EXPOSE 5080

# Directorio compartido
VOLUME /home/marcos/SigaSiga/red5test/shared

# Comando de inicio para ejecutar Red5Pro
CMD ["/bin/bash"]

