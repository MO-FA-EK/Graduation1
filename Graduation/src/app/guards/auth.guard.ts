import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private authService: AuthService, private router: Router) {}

  canActivate(): boolean {
    const isLogged = this.authService.isAuthenticated();

    if (isLogged) {
      return true; // ✅ المستخدم مسجّل دخول، نسمح له بالدخول
    } else {
      // ❌ غير مسجل، نعيد توجيهه إلى صفحة Login
      this.router.navigate(['/login']);
      return false;
    }
  }
}
