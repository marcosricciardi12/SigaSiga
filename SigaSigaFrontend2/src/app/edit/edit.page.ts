import { Component, OnInit } from '@angular/core';
import { ModalController } from '@ionic/angular';
import { ConfigTimeModalComponent } from '../config-time-modal/config-time-modal.component';
import { ScoreboardService } from '../services/scoreboard.service';
@Component({
  selector: 'app-edit',
  templateUrl: './edit.page.html',
  styleUrls: ['./edit.page.scss'],
})
export class EditPage implements OnInit {
  timer_status: boolean = false;
  tiempo: string = '00:00:0';
  reloj24: string = '00';
  puntosLocal: number = 0;
  puntosVisita: number = 0;
  periodo: number = 1;
  faltasLocal: number = 0;
  faltasVisita: number = 0;
  tiempoEnMilisegundos: number = 0;
  nombreLocal: string = '';
  nombreVisita: string = '';

  constructor(
    private modalController: ModalController,
    private scoreboardService: ScoreboardService,
  ) { }

  ngOnInit() {
  }

  play_pauseTime() {
    this.scoreboardService.change_timer_status().subscribe(
      (response:any) => {
        console.log('Respuesta del servidor:', response);
        this.timer_status = Boolean(response.timer_status)
        console.log("timer status", this.timer_status)
        // Una vez completada la lógica, actualiza la página
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }
  

  playTime() {
    this.scoreboardService.change_timer_status().subscribe(
      response => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }

  pauseTime() {
    this.scoreboardService.change_timer_status().subscribe(
      response => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }

  async configTime() {
    const modal = await this.modalController.create({
      component: ConfigTimeModalComponent
    });

    modal.onDidDismiss().then((dataReturned) => {
      if (dataReturned !== null) {
        this.tiempo = dataReturned.data.time;
        this.tiempoEnMilisegundos = dataReturned.data.milliseconds;
        console.log(`Tiempo en milisegundos: ${this.tiempoEnMilisegundos}`);
        this.scoreboardService.set_timer(this.tiempoEnMilisegundos).subscribe(
          response => {
            console.log('Respuesta del servidor:', response);
            // Una vez completada la lógica, actualiza la página
          },
          error => {
            console.error('Error al enviar la clave:', error);
          }
        );
      }
    });

    return await modal.present();
  }

  playReloj24() {
    // Lógica para iniciar el reloj de 24 segundos
  }

  pauseReloj24() {
    // Lógica para pausar el reloj de 24 segundos
  }

  resetReloj24() {
    // Lógica para reiniciar el reloj de 24 segundos
  }

  incrementPuntosLocal(value: number) {
    this.scoreboardService.add_points('local', value).subscribe(
      (response:any) => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
        this.puntosLocal = response.local_points
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }

  decrementPuntosLocal(value: number) {
    this.scoreboardService.sub_points('local', value).subscribe(
      (response:any) => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
        this.puntosLocal = response.local_points
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }

  incrementPuntosVisita(value: number) {
    this.scoreboardService.add_points('visitor', value).subscribe(
      (response:any) => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
        this.puntosVisita = response.visitor_points;
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }

  decrementPuntosVisita(value: number) {
    this.scoreboardService.sub_points('visitor', value).subscribe(
      (response:any) => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
        this.puntosVisita = response.visitor_points;
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
  }

  incrementPeriodo() {
    this.periodo++;
  }

  decrementPeriodo() {
    this.periodo--;
  }

  incrementFaltasLocal() {
    this.faltasLocal++;
  }

  decrementFaltasLocal() {
    this.faltasLocal--;
  }

  incrementFaltasVisita() {
    this.faltasVisita++;
  }

  decrementFaltasVisita() {
    this.faltasVisita--;
  }

  capturarNombres() {
    console.log(`Nombre Local: ${this.nombreLocal}`);
    console.log(`Nombre Visita: ${this.nombreVisita}`);
    const teams = {	
      "local_team": this.nombreLocal,
      "local_team_short": this.nombreLocal,
      "visitor_team": this.nombreVisita,
      "visitor_team_short": this.nombreVisita,
    };
    this.scoreboardService.set_teams(teams).subscribe(
      response => {
        console.log('Respuesta del servidor:', response);
        // Una vez completada la lógica, actualiza la página
      },
      error => {
        console.error('Error al enviar la clave:', error);
      }
    );
    // Aquí puedes añadir lógica adicional para manejar los nombres capturados
  }
}
