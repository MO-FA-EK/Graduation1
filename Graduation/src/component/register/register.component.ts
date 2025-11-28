import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { RegisterService } from '../../app/services/register.service';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-register',
  imports: [FormsModule, CommonModule, RouterModule, HttpClientModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  username = '';
  category = '';
  description = '';
  skills = '';
  portfolio = '';
  imageUrl = '';
  email = '';
  password = '';
  message = '';
  isError = false;
  isLoading = false;

  categoryOptions = [
    'Frontend Developer',
    'Backend Developer',
    'Full Stack Developer',
    'DevOps Engineer',
    'UI/UX Designer',
    'Data Scientist',
    'Mobile Developer',
    'Game Developer'
  ];

  constructor(private registerService: RegisterService, private router: Router) { }

  register() {
    if (!this.category) {
      this.message = 'Please select a category.';
      this.isError = true;
      return;
    }

    this.isLoading = true;
    const data = {
      username: this.username,
      category: this.category,
      description: this.description,
      skills: this.skills,
      portfolio: this.portfolio,
      imageUrl: this.imageUrl,
      email: this.email,
      password: this.password
    };

    this.registerService.registerDeveloper(data).subscribe({
      next: (res) => {
        this.message = res.message || 'Registration successful!';
        this.isError = false;
        this.clearForm();
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.isError = true;
        this.message = err.error?.error || 'Something went wrong!';
      },
      complete: () => (this.isLoading = false)
    });
  }

  clearForm() {
    this.username = '';
    this.category = '';
    this.description = '';
    this.portfolio = '';
    this.email = '';
    this.password = '';
  }
}
