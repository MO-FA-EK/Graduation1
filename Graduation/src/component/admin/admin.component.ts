import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../app/services/auth.service';

@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  stats = { freelancers: 0, clients: 0, projects: 0 };
  users: any[] = [];
  isLoading = true;
  activeTab: string = 'users';

  passData = { old_password: '', new_password: '', confirm_password: '' };
  passMessage = '';
  isPassError = false;
  isSaving = false;

  constructor(private http: HttpClient, private router: Router, private authService: AuthService) { }

  ngOnInit() {
    this.loadAdminData();
  }

  loadAdminData() {
    // Simulated data fetch
    setTimeout(() => {
      this.stats = { freelancers: 15, clients: 5, projects: 8 };
      this.users = [
        { id: 1, username: 'mock_freelancer_1', type: 'Freelancer', status: 'Active' },
        { id: 2, username: 'mock_client_1', type: 'Client', status: 'Active' },
      ];
      this.isLoading = false;
    }, 1000);
  }

  setTab(tab: string) {
    this.activeTab = tab;
  }

  changePasswordSubmit() {
    this.passMessage = '';
    this.isPassError = false;

    if (this.passData.new_password !== this.passData.confirm_password) {
      this.passMessage = "Passwords do not match";
      this.isPassError = true;
      return;
    }

    if (!this.passData.old_password || !this.passData.new_password) {
      this.passMessage = "Please fill all fields";
      this.isPassError = true;
      return;
    }

    this.isSaving = true;
    this.authService.changePassword({
      old_password: this.passData.old_password,
      new_password: this.passData.new_password
    }).subscribe({
      next: () => {
        this.isSaving = false;
        this.passMessage = "Password changed successfully!";
        this.passData = { old_password: '', new_password: '', confirm_password: '' };
      },
      error: (err) => {
        this.isSaving = false;
        this.passMessage = err.error?.old_password?.[0] || "Error changing password";
        this.isPassError = true;
      }
    });
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    this.router.navigate(['/login']);
  }
}
