import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-info',
  templateUrl: './info.page.html',
  styleUrls: ['./info.page.scss'],
})
export class InfoPage implements OnInit, OnDestroy {
  private apiUrl = environment.apiUrl;
  videoStreamUrl!: string;
  private authToken:any ;
  private videoElement!: HTMLVideoElement;
  private frameInterval: any;
  private imageElement!: HTMLImageElement;
  imagePath: any;

  constructor(private http: HttpClient, private _sanitizer: DomSanitizer) {}

  ngOnInit() {
    this.videoStreamUrl = `${this.apiUrl}/streaming/video_feed`;
    this.authToken = localStorage.getItem('token');
    this.videoStreamUrl = `${this.apiUrl}/streaming/video_feed?token=${this.authToken}`;
    console.log(this.videoStreamUrl)
    this.imageElement = document.getElementById('video-stream') as HTMLImageElement;
    // this.startVideoStream();
  }

  ngOnDestroy() {
    clearInterval(this.frameInterval); // Limpiar el intervalo al salir de la página
  }

  startVideoStream() {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${this.authToken}`,
      'content-type': 'application/json',
      'Access-Control-Allow-Origin': '*',
    });
      this.http.get(this.videoStreamUrl, { headers, responseType: 'blob' }).subscribe({
        next: (response: Blob) => {
          // Actualizar el src de la imagen con el blob recibido
          console.log("Hola morsilla")
          const imageUrl = URL.createObjectURL(response);
          this.imageElement.src = imageUrl;
          console.log(this.imageElement.src)
          // this.imagePath = this._sanitizer.bypassSecurityTrustResourceUrl(response);
        },
        error: (error) => {
          console.error('Error fetching video stream:', error);
        }
      });
  }
}