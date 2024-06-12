import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ScoreboardService {
  private apiUrl = environment.apiUrl;

  constructor(private router: Router, private http: HttpClient) { }

  change_timer_status() {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/scoreboard/change_play_pause_time', {}, { headers });
  }

  set_timer(time:any) {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/scoreboard/set_time/' + time.toString(), {}, { headers });
  }

  set_teams(teams:any) {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/scoreboard/set_teams', teams, { headers });
  }

  add_points(team:any, points:any) {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/scoreboard/add_point/' + team.toString() + '/' + points.toString(), {}, { headers });
  }

  sub_points(team:any, points:any) {
    const token = localStorage.getItem('token')
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    });
    return this.http.post(this.apiUrl + '/scoreboard/sub_point/' + team.toString() + '/' + points.toString(), {}, { headers });
  }
}
