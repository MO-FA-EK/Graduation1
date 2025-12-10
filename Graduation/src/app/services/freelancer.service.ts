import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
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

  // LIST ALL FREELANCERS (Services page)
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
        username: f.username,
        email: f.email,
        category: f.category,
        description: f.description,
        skills: typeof f.skills === 'string' ? f.skills.split(',') : (f.skills || []),
        portfolio: f.portfolio,
        imageUrl: f.imageUrl,
        rating: f.rating,
        totalRatings: f.totalRatings,
        profileViews: f.profileViews ?? 0,
        contactClicks: f.contactClicks ?? 0
      }));
    })
  );
}


  // SINGLE FREELANCER (Profile page)
  getFreelancerById(id: number): Observable<Freelancer> {
    return this.http.get<any>(`${this.apiUrl}${id}/`).pipe(
      map((f: any) => ({
        id: f.id,
        username: f.username,
        email: f.email,
        category: f.category,
        description: f.bio ?? f.description ?? '',
        skills: typeof f.skills === 'string'
          ? f.skills.split(',').map((s: string) => s.trim())
          : (f.skills || []),
        portfolio: f.portfolio ?? '',
        imageUrl: f.imageUrl ?? '',
        rating: f.rating ?? 0,
        totalRatings: f.totalRatings ?? 0,
        profileViews: f.profileViews ?? 0,
        contactClicks: f.contactClicks ?? 0
      }))
    );
  }

  // TRACKING: VIEWS + CONTACT CLICKS
  incrementProfileViews(id: number): Observable<number> {
    return this.http.post<any>(`${this.apiUrl}${id}/view/`, {}).pipe(
      map(res => res.profileViews ?? res.profile_views ?? 0)
    );
  }

  incrementContactClicks(id: number): Observable<number> {
    return this.http.post<any>(`${this.apiUrl}${id}/contact/`, {}).pipe(
      map(res => res.contactClicks ?? res.contact_clicks ?? 0)
    );
  }
}
