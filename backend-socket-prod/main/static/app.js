function startStreaming() {
  const urlInput = document.getElementById('urlInput').value;
  const dominio = window.location.origin;
  // Crear una nueva conexión SocketIO
  console.log(dominio)
  const socket = io(dominio);


    // Escuchar eventos de conexión y errores en el socket
    socket.on('connect', function() {
      console.log('Conexión SocketIO establecida.');
  });

  socket.on('connect_error', function(error) {
      console.error('Error en la conexión SocketIO:', error);
  });

  // Realizar la petición HTTP a la URL de la fuente de video
  fetch(urlInput)
  .then(response => {
      if (!response.ok) {
          throw new Error('No se pudo realizar la petición HTTP.');
      }
      return response.body;
  })
  .then(body => {
      // Leer y procesar los frames de video en tiempo real
      const reader = body.getReader();

      function processStream({ done, value }) {
          // Enviar cada frame de video al servidor Flask a través de SocketIO
          socket.emit('send_frame_from_client', { video_frame: value });
          // Continuar leyendo el siguiente frame de video
          return reader.read().then(processStream);
      }

      // Iniciar el procesamiento del flujo de video
      reader.read().then(processStream);
  })
  .catch(error => {
      console.error('Error:', error);
  });
}