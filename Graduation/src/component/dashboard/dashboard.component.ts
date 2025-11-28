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

  stats = {
    views: 150,
    clicks: 42,
    rating: 4.8,
    totalReviews: 24
  };

  constructor(private authService: AuthService, private router: Router) { }

  ngOnInit() {
    setTimeout(() => {
      const user = this.authService.getUser();

      if (user) {
        this.profile = user;
      } else {
        this.router.navigate(['/login']);
      }

      this.isLoading = false;
    }, 1000);
  }

  saveProfile() {
    if (!this.profile) return;
    this.isSaving = true;

    this.authService.updateUser(this.profile).subscribe({
      next: (updatedUser) => {

        this.isSaving = false;
        this.profile = updatedUser;
        alert('✅ Data saved successfully to LocalStorage!');
      },
      error: (err) => {
        this.isSaving = false;
        console.error(err);
        alert('❌ Failed to save data');
      }
    });
  }


  setTab(tab: string) {
    this.activeTab = tab;
    if (window.innerWidth <= 768) {
      this.isSidebarOpen = false;
    }
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  logout() {
    const confirmLogout = confirm('Are you sure you want to logout?');
    if (confirmLogout) {
      this.authService.logout();
      this.router.navigate(['/login']);
    }
  }
}
