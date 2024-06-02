import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class SportService {
  private apiUrl = environment.apiUrl; // URL de la API que devuelve la lista de deportes

  constructor(private http: HttpClient) {}

  getSports(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl + "/streaming/get_sports");
  }
}