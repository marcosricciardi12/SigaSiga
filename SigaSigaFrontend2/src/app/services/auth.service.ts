import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { jwtDecode, JwtPayload } from 'jwt-decode';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = environment.apiUrl;

  constructor(private router: Router, private http: HttpClient) {}

  authenticate(): Observable<any> {
    return this.http.post<any>(this.apiUrl, {}).pipe(
      tap(response => {
        if (response && response.token) {
          localStorage.setItem('token', response.token);
        }
      })
    );
  }

  create_new_event(sport_id : any): Observable<any> {
    return this.http.post<any>(this.apiUrl + "/streaming/new_event/" + sport_id.toString(), {}).pipe(
      tap(response => {
        console.log(response.event_id)
        if (response && response.token) {
          localStorage.setItem('token', response.token);
        }
      })
    );
  }


  public isAuthenticated(): boolean {
    const token = localStorage.getItem('token');
    if (!token) {
      return false;
    }

    try {
      const decodedToken: JwtPayload = jwtDecode<JwtPayload>(token);
      if (decodedToken.exp === undefined) {
        return false;
      }
      const expirationDate = new Date(decodedToken.exp * 1000);
      return expirationDate > new Date();
    } catch (error) {
      return false;
    }
  }

  public logout() {

    localStorage.removeItem('token');
    this.router.navigate(['/home']);
  }

  public stop_event() {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    console.log(headers)
    localStorage.removeItem('token');
    return this.http.post(`${this.apiUrl}/streaming/stop_event`, {}, { headers });
  }

  public authGuardFactory(): boolean {
      if (!this.isAuthenticated()) {
        console.log("hace algo(no autenticado)")
        this.router.navigate(['/home']); // Redirige al home si el usuario no está autenticado
        return false;
      }
      console.log("hace algo(autenticado)")
      return true;
  }
}
