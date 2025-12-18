import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of, tap, map, catchError } from 'rxjs';
import { Router } from '@angular/router';

export interface User {
  id: number;
  username: string;
  email: string;
  user_type?: string;
  imageUrl?: string;
  category?: string;
  description?: string;
  skills?: string | string[];
  portfolio?: string;
  profileViews?: number;
  contactClicks?: number;
  rating?: number;
  totalRatings?: number;
  bank_name?: string;
  iban?: string;
  is_superuser?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private loginUrl = 'http://localhost:8000/api/auth/login/';
  private profileUrl = 'http://localhost:8000/api/profile/';
  private changePassUrl = 'http://localhost:8000/api/auth/change-password/';

  constructor(private http: HttpClient, private router: Router) { }

  login(username: string, password: string): Observable<any> {
    return this.http.post<any>(this.loginUrl, { username, password }).pipe(
      tap(res => {
        if (res.access) {
          this.saveToken(res.access);
          if (res.user_id) {
            this.saveUser({
              id: res.user_id,
              username: res.username,
              email: res.email,
              user_type: res.user_type
            });
          }
        }
      })
    );
  }

  saveToken(token: string) { localStorage.setItem('access_token', token); }
  getToken(): string | null { return localStorage.getItem('access_token'); }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    this.router.navigate(['/login']);
  }

  isLoggedIn(): boolean { return !!this.getToken(); }
  isAuthenticated(): boolean { return this.isLoggedIn(); }

  getUser(): User | null {
    const raw = localStorage.getItem('user');
    return raw ? JSON.parse(raw) : null;
  }

  saveUser(user: any) {
    localStorage.setItem('user', JSON.stringify(user));
  }



  getUserProfile(): Observable<User | null> {
    const token = this.getToken();
    if (!token) return of(null);

    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });

    return this.http.get<any>(this.profileUrl, { headers }).pipe(
      map(data => {
        return {
          id: data.id,
          username: data.username,
          email: data.email,
          user_type: data.user_type,
          category: data.category,
          description: data.bio,
          skills: data.skills || [],
          portfolio: data.portfolio,
          imageUrl: data.image || data.imageUrl,
          rating: data.rating,
          totalRatings: data.totalRatings,
          profileViews: data.profileViews,
          contactClicks: data.contactClicks,
          bank_name: data.bank_name,
          iban: data.iban,
          is_superuser: data.is_superuser
        } as User;
      }),
      tap(user => this.saveUser(user)),
      catchError(() => of(null))
    );
  }

  updateUser(profileData: Partial<User>): Observable<User> {
    const token = this.getToken();
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });

    const payload = {
      username: profileData.username,
      bio: profileData.description,
      category: profileData.category,
      skills: profileData.skills,
      portfolio: profileData.portfolio,
      imageUrl: profileData.imageUrl,
      bank_name: profileData.bank_name,
      iban: profileData.iban
    };

    return this.http.patch<any>(this.profileUrl, payload, { headers }).pipe(
      map(updatedData => {
        const currentUser = this.getUser() || {} as User;
        const user: User = {
          ...currentUser,
          ...updatedData,
          description: updatedData.bio,
          skills: profileData.skills
        };
        this.saveUser(user);
        return user;
      })
    );
  }

  changePassword(data: any): Observable<any> {
    const token = this.getToken();
    const headers = new HttpHeaders({ 'Authorization': `Bearer ${token}` });
    return this.http.put(this.changePassUrl, data, { headers });
  }
}
