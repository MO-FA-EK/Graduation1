import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Freelancer {
  id: number;
  username: string;
  email: string;
  category: string;
  bio?: string;
  skills: string[];
  portfolio?: string;
  imageUrl?: string;
  rating: number;
  totalRatings: number;
  profileViews: number;
  contactClicks: number;
}

@Injectable({
  providedIn: 'root'
})
export class FreelancerService {

  private apiUrl = 'http://localhost:8000/api/programmers';

  constructor(private http: HttpClient) {}

  private getAuthHeaders() {
    const token = localStorage.getItem('access_token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  getFreelancers(search?: string): Observable<Freelancer[]> {
    let url = `${this.apiUrl}/`;

    if (search && search.trim() !== "") {
      url += `?search=${encodeURIComponent(search)}`;
    }

    return this.http.get<any>(url).pipe(
      map(response => {
        const results = response.results || response;
        return results.map((f: any) => this.mapFreelancer(f));
      })
    );
  }

  getFreelancerById(id: number): Observable<Freelancer> {
    return this.http.get<any>(`${this.apiUrl}/${id}/`).pipe(
      map((f: any) => this.mapFreelancer(f))
    );
  }

  incrementProfileViews(id: number): Observable<number> {
    return this.http.post<any>(`${this.apiUrl}/${id}/view/`, {}).pipe(
      map(res => res.profileViews)
    );
  }

  incrementContactClicks(id: number): Observable<number> {
    return this.http.post<any>(`${this.apiUrl}/${id}/contact/`, {}).pipe(
      map(res => res.contactClicks)
    );
  }

  rateFreelancer(id: number, stars: number): Observable<any> {
    return this.http.post<any>(
      `${this.apiUrl}/${id}/rate/`,
      { rating: stars },
      { headers: this.getAuthHeaders() }
    );
  }

  private mapFreelancer(f: any): Freelancer {
    return {
      id: f.id,
      username: f.username || f.name,
      email: f.email,
      category: f.category,
      bio: f.bio || '',
      skills: typeof f.skills === 'string' ? f.skills.split(',') : (f.skills || []),
      portfolio: f.portfolio || '',
      imageUrl: f.imageUrl || f.image || '',
      rating: f.rating || 0,
      totalRatings: f.totalRatings || 0,
      profileViews: f.profileViews || 0,
      contactClicks: f.contactClicks || 0
    };
  }
}
