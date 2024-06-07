import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { AuthService } from '../services/auth.service';
import { ParametersService } from '../services/parameters.service';
import { StreamingService } from '../services/streaming.service';
import { DomSanitizer } from '@angular/platform-browser';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.page.html',
  styleUrls: ['./settings.page.scss'],
})
export class SettingsPage implements OnInit {
  yt_rtmp_key:any;
  yt_rtmp_key_input: any;
  join_url:any;
  role:any;
  encoded_img:any
  imagePath:any;
  user_id:any;
  arrayParticipants:any;

  constructor(private navCtrl: NavController, 
    private authService: AuthService,
    private paramService: ParametersService,
    private streamingService: StreamingService,
    private _sanitizer: DomSanitizer,
  ) { }

  ngOnInit() {
    this.getParameter_rtmp_key("youtube_rtmp_key")
    this.getParticipants()
    console.log(this.yt_rtmp_key)
  }

  finalizarEvento() {
    // Aquí puedes agregar la lógica para finalizar el evento
    this.authService.stop_event().subscribe({
      next: response => {
        console.log('Evento detenido', response);
        
      },
      error: err => {
        console.error('Error de autenticación:', err);
      }
    });
    console.log('Evento finalizado');
    // Navegar a otra página si es necesario
    this.navCtrl.navigateBack('/home');
  }

  get noRtmpKey() {
    if (!this.yt_rtmp_key){
      console.log("No hay clave rtmp", this.yt_rtmp_key)
      return true
    }
    else
    {
      return false
    }
  }

  getParameter_rtmp_key(parameter: string) {
    this.paramService.getParam(parameter).subscribe((data:any) =>{
      console.log('JSON data: ', data);
      this.yt_rtmp_key = data.youtube_rtmp_key;
    });
  }

  onSendKey() {
    // Aquí colocas la lógica que deseas ejecutar con youtubeKey
    console.log("Enviar key youtube!", this.yt_rtmp_key_input)
    if(this.yt_rtmp_key_input){
      this.yt_rtmp_key = this.yt_rtmp_key_input
      this.streamingService.set_yt_rtmp_key({ "youtube_rtmp_key": this.yt_rtmp_key }).subscribe(
        response => {
          console.log('Respuesta del servidor:', response);
          // Una vez completada la lógica, actualiza la página
          this.getParameter_rtmp_key("youtube_rtmp_key")
        },
        error => {
          console.error('Error al enviar la clave:', error);
        }
      );
    }
    
  }

  refreshPage() {
    // Refresca la página actual
    window.location.reload();
  }

  onToggleChange(event: any) {
    if (event.detail.checked) {
      this.streamingService.play_yt_streaming().subscribe(
        response => {
          console.log('Respuesta del servidor:', response);
          // Una vez completada la lógica, actualiza la página
        },
        error => {
          console.error('Error al enviar la clave:', error);
        }
      );
    } else {
      this.streamingService.stop_yt_streaming().subscribe(
        response => {
          console.log('Respuesta del servidor:', response);
          // Una vez completada la lógica, actualiza la página
        },
        error => {
          console.error('Error al enviar la clave:', error);
        }
      );
    }
  }
  isModalNewParticipant = false;

  setOpenModalParticipant(isOpen: boolean) {
    this.isModalNewParticipant = isOpen;
    if (this.isModalNewParticipant){
      this.new_participant()
      this.getParticipants()
    }
  }

  new_participant(){
    const domain = window.location.host;
    const protocol = window.location.protocol;
    const web_domain = protocol + "//" + domain
    this.streamingService.add_new_participant(web_domain).subscribe((data:any) =>{
      this.join_url = data.join_url;
      this.role = data.role;
      this.user_id = data.user_id
      this.encoded_img = data.join_qr_img;
      this.imagePath = this._sanitizer.bypassSecurityTrustResourceUrl('data:image/png;base64,' 
                 + this.encoded_img);
      console.log(data)
    })
    this.getParticipants()
  }

  getParticipants(){
    this.streamingService.getParticipants().subscribe((data:any) =>{
      console.log('JSON data: ', data);
      this.arrayParticipants = data.participants;
      console.log('Paginacion actual: ', this.arrayParticipants);
    })
  }

  getParticipant(user_id:any){
    this.streamingService.getParticipant(user_id).subscribe((data:any) =>{
      this.join_url = data.join_url;
      this.role = data.role;
      this.user_id = data.user_id
      this.encoded_img = data.join_qr_img;
      this.imagePath = this._sanitizer.bypassSecurityTrustResourceUrl('data:image/png;base64,' 
                 + this.encoded_img);
      console.log(data)
    })
  }

  isModalGetParticipant = false;

  setOpenModalGetParticipant(isOpen: boolean, user_id: string) {
    this.isModalGetParticipant = isOpen;
    if (this.isModalGetParticipant){
      this.getParticipant(user_id)
    }
  }
  
}
