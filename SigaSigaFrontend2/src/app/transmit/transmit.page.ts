import { Component, ElementRef, ViewChild } from '@angular/core';
import io from 'socket.io-client';
import { environment } from '../../environments/environment';
import { StreamingService } from '../services/streaming.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-transmit',
  templateUrl: './transmit.page.html',
  styleUrls: ['./transmit.page.scss'],
})
export class TransmitPage {
  private socket: any;
  public capturing: boolean = false;
  @ViewChild('videoElement', { static: false }) videoElement?: ElementRef<HTMLVideoElement>;

  private captureInterval: any;
  private apiUrl = environment.apiUrl;
  private token:any;

  constructor(private configService: StreamingService, private http: HttpClient) {
    // Initialize socket with Flask server address
    // this.socket = io('https://192.168.54.199:5000');
    
  }

  async toggleCapture() {
    if (this.capturing) {
      this.stopCapture();
    } else {
      this.startCapture();
    }
  }

  async startCapture() {
    this.token = localStorage.getItem('token')
    console.log(this.token)
    const headers = { 'Authorization': 'Bearer ' + this.token };
    const body = { };
    this.http.post<any>(this.apiUrl + '/config/add_socket_video_source', body, { headers }).subscribe(data => {
        const datos = data;})
    // Navegar a otra página si es necesario
    this.connectWithToken(this.apiUrl);
    this.capturing = true;
    if (this.videoElement) {
      const video = this.videoElement.nativeElement;

      const constraints = {
        video: {
          facingMode: 'environment',
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      };

      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        video.play();

        this.captureInterval = setInterval(() => {
          this.captureAndSendFrame();
        }, 1000 / 30); // Capture and send a frame every 1/25 seconds (approx. 25 fps)
      } catch (error) {
        console.error('Error starting video capture:', error);
      }
    } else {
      console.error('videoElement is not defined.');
    }
  }

  stopCapture() {
    this.capturing = false;
    clearInterval(this.captureInterval);
if (this.videoElement && this.videoElement.nativeElement.srcObject) {
    const mediaStream = this.videoElement.nativeElement.srcObject as MediaStream;
    mediaStream.getTracks().forEach(track => {
      track.stop();
    });
    this.socket.stop()
  }
  }

  captureAndSendFrame() {
    if (this.videoElement) {
      const video = this.videoElement.nativeElement;
      const canvas = document.createElement('canvas');
  
      // Limitar el ancho máximo a 720 y el alto máximo a 1280
      const maxWidth = 720;
      const maxHeight = 1280;
  
      // Calcular las dimensiones del canvas manteniendo la relación de aspecto original
      let width = video.videoWidth;
      let height = video.videoHeight;
      if (width > maxWidth) {
        height = Math.round(height * maxWidth / width);
        width = maxWidth;
      }
      if (height > maxHeight) {
        width = Math.round(width * maxHeight / height);
        height = maxHeight;
      }
  
      canvas.width = width;
      canvas.height = height;
  
      const context = canvas.getContext('2d');
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/webp', 0.35);
        const base64Data = dataUrl.split(',')[1];
        this.sendFrame(base64Data);
      } else {
        console.error('Failed to get context from canvas.');
      }
    } else {
      console.error('videoElement is not defined.');
    }
  }

  sendFrame(frame: string) {
    try {
      this.socket.emit('frame', frame);
    } catch (error) {
      console.error('Error sending frame:', error);
    }
  }

  connectWithToken(socket_url: string) {
    const token = localStorage.getItem('token')
    this.socket = io(socket_url, {
      query: { token }
    });
  }

}

  
