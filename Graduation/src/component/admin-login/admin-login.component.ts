import { Component } from '@angular/core';
import { AuthService } from '../../app/services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-admin-login',
    imports: [CommonModule, FormsModule],
    templateUrl: './admin-login.component.html',
    styleUrls: ['./admin-login.component.css']
})
export class AdminLoginComponent {

    username = '';
    password = '';
    errorMessage = '';
    isLoading = false;

    constructor(
        private authService: AuthService,
        private router: Router
    ) { }

    login() {
        this.isLoading = true;
        this.errorMessage = '';

        this.authService.login(this.username, this.password).subscribe({
            next: (res) => {
                this.isLoading = false;

                if (res.access) {
                    this.authService.saveToken(res.access);

                    this.authService.saveUser({
                        id: res.user_id,
                        username: res.username,
                        email: res.email,
                        user_type: res.user_type,
                        is_superuser: res.is_superuser
                    });

                    if (res.is_superuser || res.user_type === 'admin') {
                        this.router.navigate(['/admin']);
                    } else {
                        this.errorMessage = 'Access Denied: Not an Admin';
                        this.authService.logout();
                    }
                }
            },
            error: () => {
                this.isLoading = false;
                this.errorMessage = 'Invalid admin credentials';
            }
        });

    }

}
