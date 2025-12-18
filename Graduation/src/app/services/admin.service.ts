import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, map } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class AdminService {
    private userUrl = 'http://localhost:8000/api/auth/admin/users/';
    private projectUrl = 'http://localhost:8000/api/admin/projects/';

    constructor(private http: HttpClient) { }

    private getHeaders() {
        const token = localStorage.getItem('access_token');
        return new HttpHeaders({ Authorization: `Bearer ${token}` });
    }

    getUsers(): Observable<any[]> {
        return this.http.get<any>(this.userUrl, { headers: this.getHeaders() }).pipe(
            map(response => {
                if (response && response.results) {
                    return response.results;
                }
                return Array.isArray(response) ? response : [];
            })
        );
    }

    deleteUser(id: number): Observable<any> {
        return this.http.delete(`${this.userUrl}${id}/delete/`, { headers: this.getHeaders() });
    }

    getProjects(): Observable<any[]> {
        return this.http.get<any>(this.projectUrl, { headers: this.getHeaders() }).pipe(
            map(response => {
                if (response && response.results) {
                    return response.results;
                }
                return Array.isArray(response) ? response : [];
            })
        );
    }

    deleteProject(id: number): Observable<any> {
        return this.http.delete(`${this.projectUrl}${id}/delete/`, { headers: this.getHeaders() });
    }
}
