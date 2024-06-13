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

    set_yt_rtmp_key(params: any) {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    console.log(params)
    return this.http.post(this.apiUrl + '/config/set_yt_rtmp_key', params, { headers });
  }

  play_yt_streaming() {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/streaming/start_youtube_streaming', {}, { headers });
  }

  stop_yt_streaming() {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/streaming/stop_youtube_streaming', {}, { headers });
  }

  add_new_participant(web_domain : any): Observable<any> {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post<any>(this.apiUrl + "/config/add_new_participant", {"web_url": web_domain}, { headers });
  }

  getParticipants() {
    let auth_token = localStorage.getItem('token');
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth_token}`
      });
      return this.http.get((this.apiUrl)+'/config/get_participant_list', {headers: headers});
  }

  getParticipant(user_id: any) {
    let auth_token = localStorage.getItem('token');
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth_token}`
      });
      return this.http.get((this.apiUrl)+'/config/get_participant/'+user_id.toString(), {headers: headers});
  }

  getVideoSources() {
    let auth_token = localStorage.getItem('token');
      const headers = new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${auth_token}`
      });
      return this.http.get((this.apiUrl)+'/config/get_video_sources_list', {headers: headers});
  }

  change_video_source(video_name:any) {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/streaming/change_socket_video_source/'+ video_name.toString(), {}, { headers });
  }

}
