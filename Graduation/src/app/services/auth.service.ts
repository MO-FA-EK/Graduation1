import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, of } from 'rxjs';
import { delay, tap } from 'rxjs/operators';

export interface User {
  id: number;
  username: string;
  email: string;
  category: string;
  description: string;
  skills: string; // لاحظ: هنا نص
  portfolio: string;
  imageUrl: string;
  rating: number;
  totalRatings: number;
  profileViews: number;
  contactClicks: number;
  token?: string;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private storageKey = 'mock_user';
  private freelancersKey = 'mock_freelancers'; // مفتاح قائمة الفريلانسرز

  constructor(private router: Router) { }

  // دالة تسجيل الدخول (المحدثة لتكون ذكية)
  login(email: string, pass: string): Observable<boolean> {

    // 1. محاولة البحث عن المستخدم في قائمة الفريلانسرز المسجلين
    const freelancersStr = localStorage.getItem(this.freelancersKey);
    const freelancers = freelancersStr ? JSON.parse(freelancersStr) : [];

    // نبحث عن الشخص الذي يملك نفس الإيميل
    const foundFreelancer = freelancers.find((f: any) => f.email.toLowerCase() === email.toLowerCase());

    let userToLogin: User;

    if (foundFreelancer) {
      // ✅ إذا وجدنا المستخدم المسجل، نستخدم بياناته
      userToLogin = {
        id: foundFreelancer.id,
        username: foundFreelancer.username,
        email: foundFreelancer.email,
        category: foundFreelancer.category,
        description: foundFreelancer.description,
        // تحويل المصفوفة إلى نص لأن الداشبورد يتوقع نصاً
        skills: Array.isArray(foundFreelancer.skills) ? foundFreelancer.skills.join(', ') : foundFreelancer.skills,
        portfolio: foundFreelancer.portfolio,
        imageUrl: foundFreelancer.imageUrl || 'assets/img/user.png',
        rating: foundFreelancer.rating || 0,
        totalRatings: foundFreelancer.totalRatings || 0,
        profileViews: foundFreelancer.profileViews || 0,
        contactClicks: foundFreelancer.contactClicks || 0,
        token: 'fake-jwt-token-registered'
      };
    } else {
      // ❌ إذا لم نجده، نستخدم الحساب التجريبي الافتراضي (للتسهيل)
      userToLogin = {
        id: 1,
        username: 'Hamze Developer',
        email: email, // نستخدم الايميل المدخل حتى لا يشعر المستخدم بالفرق
        category: 'Full Stack Developer',
        description: 'Senior Developer specialized in Angular & Django.',
        skills: 'Angular, TypeScript, Python, Django',
        portfolio: 'www.github.com',
        imageUrl: 'assets/img/user.png',
        rating: 4.8,
        totalRatings: 24,
        profileViews: 150,
        contactClicks: 42,
        token: 'fake-jwt-token-default'
      };
    }

    return of(true).pipe(
      delay(1000), // محاكاة الشبكة
      tap(() => {
        this.setUser(userToLogin); // حفظ المستخدم الذي تم اختياره
      })
    );
  }

  // --- بقية الدوال كما هي ---

  register(userData: any): Observable<boolean> {
    // هذه الدالة تستخدم فقط لإنشاء جلسة مباشرة بعد التسجيل (اختياري)
    return of(true).pipe(
      delay(1500),
      tap(() => {
        // تحويل البيانات لتناسب شكل المستخدم
        const newUser: User = {
          ...userData,
          id: Math.floor(Math.random() * 1000),
          imageUrl: userData.imageUrl || 'assets/img/user.png',
          rating: 0,
          totalRatings: 0,
          profileViews: 0,
          contactClicks: 0,
          token: 'fake-jwt-register-token'
        };
        this.setUser(newUser);
      })
    );
  }

  getUser(): User | null {
    const userStr = localStorage.getItem(this.storageKey);
    return userStr ? JSON.parse(userStr) : null;
  }

  updateUser(updatedData: Partial<User>): Observable<User> {
    const currentUser = this.getUser();
    if (currentUser) {
      const newUserState = { ...currentUser, ...updatedData };
      this.setUser(newUserState);
      return of(newUserState).pipe(delay(500));
    }
    return of(null as unknown as User);
  }

  isAuthenticated(): boolean {
    return !!localStorage.getItem(this.storageKey);
  }

  logout(): void {
    localStorage.removeItem(this.storageKey);
    this.router.navigate(['/login']);
  }

  private setUser(user: User): void {
    localStorage.setItem(this.storageKey, JSON.stringify(user));
  }
}
