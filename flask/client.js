$(document).ready(function() {
    var videoFrame = document.getElementById("video-frame");

    // Conectarse al endpoint SSE para recibir los frames PNG
    var eventSource = new EventSource("http:localhost:5001/video_feed");

    // Manejar los eventos recibidos
    eventSource.onmessage = function(event) {
        // Actualizar la imagen con el nuevo frame recibido
        videoFrame.src = "data:image/png;base64," + event.data;
    };

    // Manejar errores de conexión
    eventSource.onerror = function(error) {
        console.error("Error de conexión SSE:", error);
    };
});