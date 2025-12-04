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

    constructor(private http: HttpClient) { }

    getFreelancers(): Observable<Freelancer[]> {
        return this.http.get<any>(this.apiUrl).pipe(
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
                    profileViews: f.profileViews,
                    contactClicks: f.contactClicks
                }));
            })
        );
    }

    getFreelancerById(id: number): Observable<Freelancer> {
        return this.http.get<any>(`${this.apiUrl}${id}/`).pipe(
            map(f => ({
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
                profileViews: f.profileViews,
                contactClicks: f.contactClicks
            }))
        );
    }

    incrementProfileViews(id: number): void {
    }

    incrementContactClicks(id: number): void {

    }
}
