import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { RegisterService } from '../../app/services/register.service';


@Component({
  selector: 'app-register',
  imports: [FormsModule, CommonModule, RouterModule],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  userType: 'client' | 'freelancer' = 'client';

  username = '';
  email = '';
  password = '';

  category = '';
  description = '';
  skills = '';
  portfolio = '';
  imageUrl = '';

  message = '';
  isError = false;
  isLoading = false;

  categoryOptions = [
    'Frontend Developer', 'Backend Developer', 'Full Stack Developer',
    'DevOps Engineer', 'UI/UX Designer', 'Data Scientist',
    'Mobile Developer', 'Game Developer'
  ];

  constructor(private registerService: RegisterService, private router: Router) { }

  register() {


    if (this.userType === 'freelancer' && !this.category) {
      this.message = 'Please select a category.';
      this.isError = true;
      return;
    }

    this.isLoading = true;

    const data = {
      username: this.username,
      email: this.email,
      password: this.password,
      user_type: this.userType,



      category: this.userType === 'freelancer' ? this.category : '',
      description: this.userType === 'freelancer' ? this.description : '',
      skills: this.userType === 'freelancer' ? this.skills : '',
      portfolio: this.userType === 'freelancer' ? this.portfolio : '',
      imageUrl: this.userType === 'freelancer' ? this.imageUrl : ''
    };

    this.registerService.registerDeveloper(data).subscribe({
      next: (res) => {
        this.message = res.message || 'Registration successful!';
        this.isError = false;
        this.router.navigate(['/login']);
      },
      error: (err) => {
        this.isError = true;
        this.message = err.error?.error || 'Something went wrong!';
        this.isLoading = false;
      }
    });
  }
}
