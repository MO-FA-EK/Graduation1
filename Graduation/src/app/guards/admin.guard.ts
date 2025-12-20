import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class AdminGuard implements CanActivate {

    constructor(private authService: AuthService, private router: Router) { }

    canActivate(): boolean | UrlTree | Observable<boolean | UrlTree> {
        const user = this.authService.getUser();
        if (user && (user.is_superuser || user.user_type === 'admin')) {
            return true;
        }
        return this.router.createUrlTree(['/admin/login']);
    }
}
