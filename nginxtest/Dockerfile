# Usa una imagen base de NGINX
FROM nginx:latest

# Instala las herramientas necesarias para compilar NGINX
RUN apt-get update && apt-get install -y \
    build-essential \
    libpcre3-dev \
    zlib1g-dev \
    libssl-dev \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Descarga NGINX
RUN wget http://nginx.org/download/nginx-1.21.5.tar.gz && \
    tar -zxvf nginx-1.21.5.tar.gz && \
    rm nginx-1.21.5.tar.gz

# Descarga el módulo RTMP para NGINX
RUN wget https://github.com/arut/nginx-rtmp-module/archive/master.zip && \
    unzip master.zip && \
    rm master.zip

# Compila NGINX con el módulo RTMP
RUN cd nginx-1.21.5 && \
    ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module-master && \
    make && \
    make install

# Copia la configuración de NGINX
COPY nginx.conf /usr/local/nginx/conf/nginx.conf
COPY index.html /usr/local/nginx/html/index.html
COPY play_hls.js /usr/local/nginx/html/play_hls.js

# Expone los puertos RTMP (1935) y HTTP (80)
EXPOSE 1935
EXPOSE 80

# Inicia NGINX
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]
