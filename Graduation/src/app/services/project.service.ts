import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Project {
  id: number;
  client: number;
  client_name: string;
  freelancer: number;
  freelancer_name: string;
  freelancer_id: number;
  title: string;
  description: string;
  github_link?: string;
  status: 'pending' | 'active' | 'completed' | 'cancelled';
  is_paid: boolean;
  amount: number;
  created_at: string;
}

@Injectable({
  providedIn: 'root'
})
export class ProjectService {
  private apiUrl = 'http://localhost:8000/api/projects/';

  constructor(private http: HttpClient) {}

  private getHeaders() {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  createProject(freelancerId: number, data: { title: string, description: string }): Observable<Project> {
    return this.http.post<Project>(`${this.apiUrl}create/${freelancerId}/`, data, { headers: this.getHeaders() });
  }

  getMyProjects(): Observable<{ hired_projects: Project[], work_projects: Project[] }> {
    return this.http.get<{ hired_projects: Project[], work_projects: Project[] }>(`${this.apiUrl}my/`, { headers: this.getHeaders() });
  }

  updateProject(projectId: number, data: any): Observable<Project> {
    return this.http.patch<Project>(`${this.apiUrl}${projectId}/update/`, data, { headers: this.getHeaders() });
  }

  createPaymentIntent(projectId: number): Observable<any> {
    const baseUrl = this.apiUrl.replace('projects/', 'payment/');
    return this.http.post<any>(
      `${baseUrl}create/${projectId}/`,
      {},
      { headers: this.getHeaders() }
    );
  }

  confirmPaymentOnServer(paymentIntentId: string): Observable<any> {
    const baseUrl = this.apiUrl.replace('projects/', 'payment/');
    return this.http.post<any>(
      `${baseUrl}confirm/`,
      { paymentIntentId },
      { headers: this.getHeaders() }
    );
  }
}
