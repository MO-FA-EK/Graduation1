import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService, User } from '../../app/services/auth.service';

@Component({
  selector: 'app-dashboard',
  imports: [FormsModule, CommonModule],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  activeTab: string = 'profile';
  isLoading: boolean = true;
  isSaving: boolean = false;
  isSidebarOpen: boolean = false;

  profile: User | null = null;

//Password change variables
  passData = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  };
  passMessage = '';
  isPassError = false;

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit() {
    this.profile = this.authService.getUser();

    this.authService.getUserProfile().subscribe({
      next: (user) => {
        if (user) {
          this.profile = user;
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
        if (!this.profile) this.router.navigate(['/login']);
      }
    });
  }

  saveProfile() {
    if (!this.profile) return;
    this.isSaving = true;

    this.authService.updateUser(this.profile).subscribe({
      next: (updatedUser: User) => {
        this.isSaving = false;
        this.profile = updatedUser;
        alert('✅ Profile updated successfully!');
      },
      error: (err: any) => {
        this.isSaving = false;
        console.error(err);
        alert('❌ Failed to update profile.');
      }
    });
  }


//Password change function
  changePasswordSubmit() {
    this.passMessage = '';
    this.isPassError = false;

    if (this.passData.new_password !== this.passData.confirm_password) {
      this.passMessage = "New passwords do not match!";
      this.isPassError = true;
      return;
    }

    if (this.passData.new_password.length < 6) {
      this.passMessage = "Password must be at least 6 characters.";
      this.isPassError = true;
      return;
    }

    this.isSaving = true;

    this.authService.changePassword({
      old_password: this.passData.old_password,
      new_password: this.passData.new_password
    }).subscribe({
      next: (res) => {
        this.isSaving = false;
        this.passMessage = res.message || "Password Changed Successfully!";
        this.isPassError = false;
        this.passData = { old_password: '', new_password: '', confirm_password: '' };
      },
      error: (err) => {
        this.isSaving = false;
        this.isPassError = true;
        this.passMessage = err.error?.old_password?.[0] || "Failed to update password.";
      }
    });
  }

  setTab(tab: string) {
    this.activeTab = tab;
    if (window.innerWidth <= 768) this.isSidebarOpen = false;
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  logout() {
    if (confirm('Are you sure you want to logout?')) {
      this.authService.logout();
    }
  }
}
