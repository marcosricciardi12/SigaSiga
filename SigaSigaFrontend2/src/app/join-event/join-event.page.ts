import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-join-event',
  templateUrl: './join-event.page.html',
  styleUrls: ['./join-event.page.scss'],
})
export class JoinEventPage implements OnInit {
  private apiUrl = environment.apiUrl;
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient,
  ) {
  }

  ngOnInit() {
    // Obtener el parámetro de la URL
    const domain = window.location.host;
    const protocol = window.location.protocol;
    const full_domain = protocol + "//" + domain

    this.route.queryParams.subscribe(params => {
      const paramValue = params['user_id'];
      console.log(paramValue)
      if (paramValue) {
        this.sendPostRequest(paramValue);
      } else {
        // Manejar el caso donde no hay un parámetro
        console.error('No parameter found in the URL');
      }
    });
  }

  sendPostRequest(user_id: string) {
    const url = this.apiUrl + '/config/join_event/' + user_id; // Reemplaza con tu URL de backend
    this.http.post<{ token: string }>(url, {})
      .subscribe(async (response) => {
        const token = response.token;
        if (token) {
          // Guardar el token en el local storage
          await localStorage.setItem('token', token);
          // Redirigir al home
          this.router.navigate(['/home']);
        } else {
          console.error('No token found in the response');
        }
      }, error => {
        console.error('Error during POST request', error);
      });
  }
}
