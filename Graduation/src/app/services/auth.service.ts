import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable, tap, of, map, catchError } from 'rxjs';



export interface User {
  id: number;
  username: string;
  email: string;
  category?: string;
  description?: string;
  skills?: string;
  portfolio?: string;
  imageUrl?: string;
  rating?: number;
  totalRatings?: number;
  profileViews?: number;
  contactClicks?: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private loginUrl = 'http://localhost:8000/api/auth/login/';
  private profileUrl = 'http://localhost:8000/api/profile/';

  private userKey = 'current_user';
  private tokenKey = 'access_token';

  constructor(private http: HttpClient, private router: Router) { }


  login(email: string, pass: string): Observable<boolean> {
    return this.http.post<any>(this.loginUrl, { username: email, password: pass }).pipe(
      tap(response => {


        if (response.access) {
            localStorage.setItem(this.tokenKey, response.access);
        }

        if (response.user) {
          localStorage.setItem(this.userKey, JSON.stringify(response.user));
        }
      }),
      map(() => true),
      catchError(error => {
        console.error('Login error:', error);
        return of(false);
      })
    );
  }



  getUserProfile(): Observable<User | null> {
    const token = this.getToken();
    if (!token) return of(null);

    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    return this.http.get<any>(this.profileUrl, { headers }).pipe(
      map(data => {

        return {
          id: data.id,
          username: data.username,
          email: data.email,
          category: data.category,
          description: data.description,
          skills: data.skills,
          portfolio: data.portfolio,
          imageUrl: data.imageUrl,
          rating: data.rating,
          totalRatings: data.totalRatings,
          profileViews: data.profileViews,
          contactClicks: data.contactClicks
        } as User;
      }),
      catchError(() => of(null))
    );
  }


  updateUser(updatedData: any): Observable<any> {
    const token = this.getToken();
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });

    const payload = {
      name: updatedData.username,
      bio: updatedData.description,
      category: updatedData.category,
      skills: updatedData.skills,
      portfolio: updatedData.portfolio
    };

    return this.http.patch(this.profileUrl, payload, { headers });
  }

  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }

  getUser(): User | null {
    const userStr = localStorage.getItem(this.userKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  isAuthenticated(): boolean {
    return !!this.getToken();
  }

  logout(): void {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.userKey);
    this.router.navigate(['/login']);
  }
}
