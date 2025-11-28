import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../app/services/auth.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, RouterModule, CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email = '';
  password = '';
  message = '';
  isError = false;
  isLoading = false;

  constructor(private auth: AuthService, private router: Router) { }

  login() {
    this.isLoading = true;
    this.auth.login(this.email, this.password).subscribe({
      next: (success) => {
        if (success) {
          this.router.navigate(['/dashboard']);
        } else {
          this.isError = true;
          this.message = 'Invalid credentials!';
        }
        this.isLoading = false;
      },
      error: () => {
        this.isError = true;
        this.message = 'Something went wrong!';
        this.isLoading = false;
      }
    });
  }
}
