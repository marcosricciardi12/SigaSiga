// http://192.168.54.198:5000
import { Component, ElementRef, ViewChild } from '@angular/core';
import io from 'socket.io-client';

@Component({
  selector: 'app-transmitir',
  templateUrl: './transmitir.page.html',
  styleUrls: ['./transmitir.page.scss'],
})
export class TransmitirPage {
  private socket: any;
  public capturando: boolean = false;
  @ViewChild('videoElement', { static: false }) videoElement?: ElementRef<HTMLVideoElement>; // Adding '?' makes it optional

  private intervaloCaptura: any;

  constructor() {
    // Inicializar el socket con la dirección del servidor Flask
    this.socket = io('https://192.168.54.198:5000');
  }

  async toggleCaptura() {
    if (this.capturando) {
      this.detenerCaptura();
    } else {
      this.iniciarCaptura();
    }
  }

  async iniciarCaptura() {
    this.capturando = true;
    if (this.videoElement) { // Check if videoElement is defined
      const video = this.videoElement.nativeElement;

      const constraints = {
        video: {
          facingMode: 'environment', // Usa la cámara trasera del dispositivo si está disponible
          width: { min: 1280 },
          height: { min: 720 },
          frameRate: { ideal: 25 } // Ajusta la tasa de fotogramas a 25 fps
        }
      };

      try {
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        video.srcObject = stream;
        video.play();

        this.intervaloCaptura = setInterval(() => {
          this.capturarYEnviarFrame();
        }, 1000 / 25); // Capturar y enviar un frame cada 1/25 segundos (25 fps)
      } catch (error) {
        console.error('Error al iniciar la captura de video:', error);
      }
    } else {
      console.error('videoElement is not defined.');
    }
  }

  detenerCaptura() {
    this.capturando = false;
    clearInterval(this.intervaloCaptura);
  }

  capturarYEnviarFrame() {
    if (this.videoElement) { // Check if videoElement is defined
      const video = this.videoElement.nativeElement;
      const canvas = document.createElement('canvas');
      canvas.width = 720;
      canvas.height = 1280;
      const context = canvas.getContext('2d');
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const frame = canvas.toDataURL('image/jpeg');
        this.enviarFrame(frame);
      } else {
        console.error('Failed to get context from canvas.');
      }
    } else {
      console.error('videoElement is not defined.');
    }
  }

  enviarFrame(frame: string) {
    try {
      this.socket.emit('frame2', frame);
    } catch (error) {
      console.error('Error al enviar frame:', error);
    }
  }
}
