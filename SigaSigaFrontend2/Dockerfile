# Usa una imagen base de Nginx
FROM nginx:alpine

# Copia los archivos de la build de Ionic a la carpeta de Nginx
COPY ./www /usr/share/nginx/html

# Copia la configuración de Nginx
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80
EXPOSE 80

# Inicia Nginx
CMD ["nginx", "-g", "daemon off;"]
