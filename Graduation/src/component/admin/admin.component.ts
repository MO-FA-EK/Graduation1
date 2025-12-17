import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../app/services/auth.service';
import { AdminService } from '../../app/services/admin.service';

@Component({
  selector: 'app-admin',
  imports: [CommonModule, FormsModule],
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  stats = { freelancers: 0, clients: 0, projects: 0 };
  users: any[] = [];
  projects: any[] = [];
  isLoading = true;
  activeTab: string = 'users';

  passData = { old_password: '', new_password: '', confirm_password: '' };
  passMessage = '';
  isPassError = false;
  isSaving = false;

  constructor(private adminService: AdminService, private router: Router, private authService: AuthService) { }

  ngOnInit() {
    this.loadUsers();
    this.loadProjects();
  }

  loadUsers() {
    this.adminService.getUsers().subscribe({
      next: (data) => {
        console.log('Users data received:', data);
        this.users = data;
        this.stats.freelancers = data.filter(u => u.user_type === 'freelancer').length;
        this.stats.clients = data.filter(u => u.user_type === 'client').length;
        console.log('Stats updated:', this.stats);
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading users:', err);
        this.isLoading = false;
      }
    });
  }

  loadProjects() {
    this.adminService.getProjects().subscribe({
      next: (data) => {
        console.log('Projects data received:', data);
        this.projects = data;
        this.stats.projects = data.length;
        this.isLoading = false;
      },
      error: (err) => {
        console.error('Error loading projects:', err);
        this.isLoading = false;
      }
    });
  }

  deleteUser(id: number) {
    if (!confirm('Are you sure you want to delete this user?')) return;
    this.adminService.deleteUser(id).subscribe(() => {
      alert('User deleted');
      this.loadUsers();
    });
  }

  deleteProject(id: number) {
    if (!confirm('Delete this project?')) return;
    this.adminService.deleteProject(id).subscribe(() => {
      alert('Project deleted');
      this.loadProjects();
    });
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
