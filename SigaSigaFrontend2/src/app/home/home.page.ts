import { Component, OnInit } from '@angular/core';
import { AuthService } from '../services/auth.service';
import { Router } from '@angular/router';
import { SportService } from '../services/sport.service'; // Importa el servicio de deportes

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  selectedSport: any; // Variable para almacenar el deporte seleccionado
  sports: any;  // Arreglo para almacenar la lista de deportes

  constructor(
    private authService: AuthService,
    private router: Router,
    private sportService: SportService // Inyecta el servicio de deportes
  ) {}

  ngOnInit() {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/menu']); // Redirigir a otra página si el usuario está autenticado
    } else {
      console.log("No hay usuario válido logueado");
    }

    // Llama al método para obtener la lista de deportes al inicializar el componente
    this.loadSports();
  }

  handleButtonClick() {
    // Implementa tu lógica aquí
    if (this.selectedSport) {
      console.log('Botón presionado');
    console.log('Deporte id seleccionado: ', this.selectedSport.id)
    this.authService.create_new_event(this.selectedSport.id).subscribe({
      next: response => {
        console.log('Evento Creado existosamente:', response);
        
        this.router.navigate(['/menu']); // Redirigir a otra página después de autenticarse
        
      },
      error: err => {
        console.error('Error de autenticación:', err);
      }
    });
    }
    else {
      console.log("No hay deporte seleccionado!");
    }
    
  }

  // Método para obtener la lista de deportes
  loadSports() {
    this.sportService.getSports().subscribe({
      next: response => {
        this.sports = response; // Almacena la lista de deportes en la variable correspondiente
        this.sports = this.sports.sports
        console.log(this.sports)
      },
      error: err => {
        console.error('Error al obtener la lista de deportes:', err);
      }
    });
  }
}
