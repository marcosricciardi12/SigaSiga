const videoPlayer = document.getElementById('videoPlayer');

// URL del video HTTP
const videoUrl = 'http://127.0.0.1:5000/video_feed';

// Función para cargar el video
async function loadVideo() {
    try {
        const response = await fetch(videoUrl);
        if (!response.ok) {
            throw new Error('No se pudo obtener el video');
        }

        const reader = response.body.getReader();
        const readerStream = new ReadableStream({
            start(controller) {
                function pushData() {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            controller.close();
                            return;
                        }
                        controller.enqueue(value);
                        pushData();
                    }).catch(error => {
                        console.error('Error al leer datos:', error);
                        controller.error(error);
                    });
                }
                pushData();
            }
        });

        const videoStream = new MediaStream();
        const videoTrack = videoStream.getVideoTracks()[0];

        const mediaSource = new MediaSource();
        videoPlayer.src = URL.createObjectURL(mediaSource);

        mediaSource.addEventListener('sourceopen', () => {
            const sourceBuffer = mediaSource.addSourceBuffer('video/mp4; codecs="avc1.42E01E"');

            sourceBuffer.addEventListener('updateend', () => {
                if (!videoTrack.enabled) {
                    videoTrack.enabled = true;
                    videoPlayer.play();
                }
            });

            readerStream.pipeTo(sourceBuffer);
        });

    } catch (error) {
        console.error('Error al cargar el video:', error);
    }
}

// Cargar el video cuando se cargue la página
window.onload = loadVideo;