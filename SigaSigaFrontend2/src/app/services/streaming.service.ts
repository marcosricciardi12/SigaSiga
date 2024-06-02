import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StreamingService {

  private apiUrl = environment.apiUrl;

  
  constructor(private router: Router, private http: HttpClient) { }

  public add_socket_video() {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(`${this.apiUrl} + '/config/add_socket_video_source'`, {}, { headers });
  }
  
  create_new_event(sport_id : any): Observable<any> {
    return this.http.post<any>(this.apiUrl + "/streaming/add_socket_video_source", {}).pipe(
      tap(response => {
        console.log(response.event_id)
        if (response && response.token) {
          localStorage.setItem('token', response.token);
        }
      })
    );
  }

}
