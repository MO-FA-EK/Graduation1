import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';
import { Observable, map } from 'rxjs';

export interface Freelancer {
  id: number;
  username: string;
  email: string;
  category: string;
  description: string;
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
  private apiUrl = 'http://localhost:8000/api/programmers/';

  constructor(private http: HttpClient) {}


  //Fetch the list and search
  getFreelancers(search?: string): Observable<Freelancer[]> {
    let url = this.apiUrl;
    if (search && search.trim() !== "") {
      url = `${this.apiUrl}?search=${encodeURIComponent(search)}`;
    }

    return this.http.get<any>(url).pipe(
      map(response => {
        const results = response.results || response;
        return results.map((f: any) => ({
          id: f.id,
          username: f.username || f.name,
          email: f.email,
          category: f.category,
          description: f.bio || f.description || '',
          skills: typeof f.skills === 'string' ? f.skills.split(',') : (f.skills || []),
          portfolio: f.portfolio,
          imageUrl: f.image || f.imageUrl,
          rating: f.rating,
          totalRatings: f.review_count || f.totalRatings || 0,
          profileViews: f.profile_views ?? 0,
          contactClicks: f.contact_clicks ?? 0
        }));
      })
    );
  }


  // 2. Retrieve details of one programmer
  getFreelancerById(id: number): Observable<Freelancer> {
    return this.http.get<any>(`${this.apiUrl}${id}/`).pipe(
      map((f: any) => ({
        id: f.id,
        username: f.username || f.name,
        email: f.email,
        category: f.category,
        description: f.bio || f.description || '',
        skills: typeof f.skills === 'string' ? f.skills.split(',') : (f.skills || []),
        portfolio: f.portfolio || '',
        imageUrl: f.image || f.imageUrl || '',
        rating: f.rating || 0,
        totalRatings: f.review_count || 0,
        profileViews: f.profile_views || 0,
        contactClicks: f.contact_clicks || 0
      }))
    );
  }
  //Increase views
  incrementProfileViews(id: number): Observable<number> {
    return this.http.post<any>(`${this.apiUrl}${id}/view/`, {}).pipe(
      map(res => res.profileViews)
    );
  }


  //Increase clicks
  incrementContactClicks(id: number): Observable<number> {
    return this.http.post<any>(`${this.apiUrl}${id}/contact/`, {}).pipe(
      map(res => res.contactClicks)
    );
  }


   //Evaluation
  rateFreelancer(id: number, rating: number): Observable<any> {
    // Fetch tokens from local storage
    const token = localStorage.getItem('access_token');


   // Add it to the header
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    return this.http.post<any>(`${this.apiUrl}${id}/rate/`, { rating }, { headers });
  }
}
