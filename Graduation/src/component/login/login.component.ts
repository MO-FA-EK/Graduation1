import { Component } from '@angular/core';
import { AuthService } from '../../app/services/auth.service';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-login',
  standalone: true,
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
  ) {}

  login() {
  this.isLoading = true;
  this.errorMessage = '';

  this.authService.login(this.username, this.password).subscribe({
    next: (res) => {
      this.isLoading = false;

      if (res.token) {
        // 1) Save token
        this.authService.saveToken(res.token);

        // 2) Save user info (so dashboard & profile can use it)
        this.authService.saveUser({
          id: res.user_id,
          username: res.username,
          email: res.email,
          user_type: res.user_type   // if backend sends it
        });

        // 3) Redirect to dashboard
        this.router.navigate(['/dashboard']);
      }
    },
    error: (err) => {
      this.isLoading = false;
      this.errorMessage = 'Invalid username or password';
    }
  });
}

}
