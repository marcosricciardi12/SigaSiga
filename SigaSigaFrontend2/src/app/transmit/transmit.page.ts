import { Component, ElementRef, ViewChild } from '@angular/core';
import io from 'socket.io-client';

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

  constructor() {
    // Initialize socket with Flask server address
    this.socket = io('https://192.168.54.199:5000');
  }

  async toggleCapture() {
    if (this.capturing) {
      this.stopCapture();
    } else {
      this.startCapture();
    }
  }

  async startCapture() {
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
        }, 1000 / 60); // Capture and send a frame every 1/25 seconds (approx. 25 fps)
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
  }
  }

  captureAndSendFrame() {
    if (this.videoElement) {
      const video = this.videoElement.nativeElement;
      const canvas = document.createElement('canvas');
      canvas.width = 720;
      canvas.height = 1280;
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
}
