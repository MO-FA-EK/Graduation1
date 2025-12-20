import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://localhost:8000/api/admin/';

  constructor(private http: HttpClient) { }

  private getHeaders() {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  getUsers(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}users/`, { headers: this.getHeaders() });
  }

  getProjects(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}projects/`, { headers: this.getHeaders() });
  }

  // 👇 هذه الدالة كانت مفقودة وتسبب الخطأ
  getMessages(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}messages/`, { headers: this.getHeaders() });
  }

  deleteUser(userId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}users/${userId}/`, { headers: this.getHeaders() });
  }

  deleteProject(projectId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}projects/${projectId}/`, { headers: this.getHeaders() });
  }
}