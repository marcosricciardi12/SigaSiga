if (Hls.isSupported()) {
    var video = document.getElementById('video');
    var hls = new Hls();
    var currentURL = window.location.href;
    var video_url = currentURL + 'hls/stream.m3u8';
    console.log(video_url); 
    hls.loadSource(video_url);
    hls.attachMedia(video);
    hls.on(Hls.Events.MANIFEST_PARSED, function() {
        video.play();
    });
}