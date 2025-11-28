import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of, delay, tap } from 'rxjs';
import { FreelancerService } from './freelancer.service';

@Injectable({ providedIn: 'root' })
export class RegisterService {
  private apiUrl = 'https://your-backend-api/register'; // رابط ثابت

  constructor(private http: HttpClient, private freelancerService: FreelancerService) { }

  // تسجيل (Mock)
  registerDeveloper(data: any): Observable<any> {
    // محاكاة تأخير الشبكة
    return of({ message: 'Registration successful!' }).pipe(
      delay(500),
      tap(() => {
        console.log('Mock Registration Data:', data);
        this.freelancerService.addFreelancer(data);
      })
    );
  }
}
