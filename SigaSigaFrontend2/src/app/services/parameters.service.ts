import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ParametersService {

  private apiUrl = environment.apiUrl; // URL de la API que devuelve la lista de deportes

  constructor(private httpClient: HttpClient) { }

  getParam(parameter: any) {
    let auth_token = localStorage.getItem('token');
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${auth_token}`
    });
    return  this.httpClient.get(this.apiUrl + "/config/get_parameter/" + parameter, {headers: headers});
  }
    
  }

