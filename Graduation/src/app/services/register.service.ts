import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class RegisterService {

  private apiUrl = 'http://localhost:8000/api/auth/register/';

  constructor(private http: HttpClient) { }

  registerDeveloper(data: any): Observable<any> {


    const formData = new FormData();


    formData.append('username', data.username);
    formData.append('email', data.email);
    formData.append('password', data.password);

    if (data.user_type) {
      formData.append('user_type', data.user_type);
    }

    if (data.category) formData.append('category', data.category);
    if (data.description) formData.append('description', data.description);
    if (data.skills) formData.append('skills', data.skills);
    if (data.portfolio) formData.append('portfolio', data.portfolio);
    formData.append('experience_level', 'Beginner');


    if (data.imageUrl) {
        formData.append('image', data.imageUrl);
    }

    return this.http.post(this.apiUrl, formData);
  }
}
