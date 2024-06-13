import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { DomSanitizer } from '@angular/platform-browser';
import { StreamingService } from '../services/streaming.service';
import { interval, mergeMap } from 'rxjs';
import io from 'socket.io-client';



@Component({
  selector: 'app-director',
  templateUrl: './director.page.html',
  styleUrls: ['./director.page.scss'],
})
export class DirectorPage implements OnInit, OnDestroy {
  private apiUrl = environment.apiUrl;
  videoStreamUrl!: string;
  private authToken:any ;
  private videoElement!: HTMLVideoElement;
  private frameInterval: any;
  private imageElement!: HTMLImageElement;
  private socket: any;
  imagePath: any;
  video_source_array:any;

  constructor(private http: HttpClient, 
              private _sanitizer: DomSanitizer,
              private streamingService: StreamingService,) {}

  ngOnInit() {
    const domain = window.location.host;
    const protocol = window.location.protocol;
    const full_domain = protocol + "//" + domain

    this.authToken = localStorage.getItem('token');
    // this.videoStreamUrl = `${full_domain}${this.apiUrl}/streaming/video_feed?token=${this.authToken}`;
    this.videoStreamUrl = `${this.apiUrl}/streaming/video_feed?token=${this.authToken}`;
    console.log(this.videoStreamUrl)

    this.streamingService.getVideoSources().subscribe((data:any) =>{
      console.log('JSON data: ', data);
      this.video_source_array = data;
      this.video_source_array.forEach((item: any) => {
        item.video_URL = `${this.apiUrl}/streaming/video_feed_source/${item.title}?token=${this.authToken}`;
      })
      console.log('Paginacion actual: ', this.video_source_array);
    })

    this.connectWithToken(this.apiUrl);
    this.socket.emit('director_room_join');
    this.socket.on('directors_notification', (data:any) => {
      this.video_source_array = [];
      console.log('Notificación recibida: ' + data.video_list);
      // Reemplazar True y False por true y false
      const correctedJsonString = data.video_list.replace(/True/g, 'true').replace(/False/g, 'false');
      // Reemplazar comillas simples por comillas dobles
      const finalJsonString = correctedJsonString.replace(/'/g, '"');
      const array = JSON.parse(finalJsonString);
      array.forEach((item: any) => {
        item.video_URL = `${this.apiUrl}/streaming/video_feed_source/${item.title}?token=${this.authToken}`;
      });
      this.delay(1000).then(() => {
        this.video_source_array = array;
      });
      
      
      console.log('Paginacion actual: ', this.video_source_array);
  });
  }

  ngOnDestroy() {
    clearInterval(this.frameInterval); // Limpiar el intervalo al salir de la página
  }



  toggleChanged(activeIndex: number) {
    this.video_source_array.forEach((card:any, index:any) => {
      card.active = index === activeIndex;
      const video_name = this.video_source_array[activeIndex]['title'];
      console.log("nombre de la fuente de video: ", video_name);
      this.streamingService.change_video_source(video_name).subscribe(
        response => {
          console.log('Respuesta del servidor:', response);
          // Una vez completada la lógica, actualiza la página
        },
        error => {
          console.error('Error al enviar la clave:', error);
        }
      );
    });
  }

  getVideoSources(){
    this.streamingService.getVideoSources().subscribe((data:any) =>{
      console.log('JSON data: ', data);
      this.video_source_array = data;
      this.video_source_array.forEach((item: any) => {
        item.video_URL = `${this.apiUrl}/streaming/video_feed_source/${item.title}?token=${this.authToken}`;
      })
      console.log('Paginacion actual: ', this.video_source_array);
    })
  }

  connectWithToken(socket_url: string) {
    const token = localStorage.getItem('token')
    console.log(socket_url)
    this.socket = io(socket_url, {
      query: { token }
    });
  }

  delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
}