import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';

export interface User {
  id: number;
  username: string;
  email: string;
  user_type?: string;

  // Extra freelancer/dashboard fields (all optional)
  imageUrl?: string;
  category?: string;
  description?: string;
  skills?: string | string[];   // can be string or array
  portfolio?: string;

  profileViews?: number;
  contactClicks?: number;
  rating?: number;
  totalRatings?: number;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user_id: number;
  username: string;
  email: string;
  user_type?: string;
}



@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loginUrl = 'http://localhost:8000/api/auth/login/';
  private profileUrl = 'http://localhost:8000/api/profile/'; // for future

  constructor(private http: HttpClient) { }

  // -------- LOGIN --------
  login(username: string, password: string): Observable<LoginResponse> {
  return this.http.post<LoginResponse>(this.loginUrl, {
    username: username,
    password: password
  });
}


saveToken(token: string) {
  localStorage.setItem('access_token', token);
}

getToken(): string | null {
  return localStorage.getItem('access_token');
}


  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // Used by AuthGuard
  isLoggedIn(): boolean {
    return !!this.getToken();
  }

  // Keep compatibility with old code
  isAuthenticated(): boolean {
    return this.isLoggedIn();
  }

  // -------- USER HANDLING (for dashboard) --------
  saveUser(user: User) {
    localStorage.setItem('user', JSON.stringify(user));
  }

  getUser(): User | null {
    const raw = localStorage.getItem('user');
    if (!raw) return null;
    try {
      return JSON.parse(raw) as User;
    } catch {
      return null;
    }
  }

  // Fake update for now: update local copy and return it as Observable
  updateUser(profile: Partial<User>): Observable<User> {
    const current = this.getUser();
    if (!current) {
      // in real app you might call backend here
      const fallback: User = {
        id: 0,
        username: profile.username || '',
        email: profile.email || '',
        user_type: profile.user_type
      };
      this.saveUser(fallback);
      return of(fallback);
    }

    const updated: User = {
      ...current,
      ...profile,
    };

    this.saveUser(updated);
    return of(updated);
  }
}
