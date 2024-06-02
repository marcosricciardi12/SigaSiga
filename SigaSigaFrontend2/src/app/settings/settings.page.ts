import { Component, OnInit } from '@angular/core';
import { NavController } from '@ionic/angular';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-settings',
  templateUrl: './settings.page.html',
  styleUrls: ['./settings.page.scss'],
})
export class SettingsPage implements OnInit {

  constructor(private navCtrl: NavController, private authService: AuthService) { }

  ngOnInit() {
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

}
