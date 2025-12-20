import { Component } from '@angular/core';
import { AuthService } from '../../app/services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

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
            user_type: res.user_type
          });

          if (res.is_superuser || res.user_type === 'admin') {
            this.errorMessage = 'Admins must use the Admin Portal';
            this.authService.logout();
            this.isLoading = false;
          } else {
            console.log('Login: Redirecting to Dashboard');
            this.router.navigate(['/dashboard']);
          }
        }
      },
      error: () => {
        this.isLoading = false;
        this.errorMessage = 'Invalid username or password';
      }
    });

  }

}
