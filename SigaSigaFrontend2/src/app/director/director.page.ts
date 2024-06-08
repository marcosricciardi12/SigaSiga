import { Component, OnInit, OnDestroy } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { DomSanitizer } from '@angular/platform-browser';
import { StreamingService } from '../services/streaming.service';
import { interval, mergeMap } from 'rxjs';

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

    interval(1*1000).pipe(
      mergeMap(() => this.streamingService.getVideoSources())
    ).subscribe((data:any) =>{
      console.log('JSON data: ', data);
      this.video_source_array = data;
      this.video_source_array.forEach((item: any) => {
        item.video_URL = `${this.apiUrl}/streaming/video_feed_source/${item.title}?token=${this.authToken}`;
      })
      console.log('Paginacion actual: ', this.video_source_array);
    })
  }

  ngOnDestroy() {
    clearInterval(this.frameInterval); // Limpiar el intervalo al salir de la página
  }



  toggleChanged(activeIndex: number) {
    this.video_source_array.forEach((card:any, index:any) => {
      card.active = index === activeIndex;
      this.streamingService.change_video_source(activeIndex).subscribe(
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
}