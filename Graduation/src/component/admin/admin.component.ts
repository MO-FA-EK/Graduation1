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
  stats = { freelancers: 0, clients: 0, projects: 0, messages: 0 };
  users: any[] = [];
  projects: any[] = [];
  messages: any[] = [];
  isLoading = true;
  activeTab: string = 'users';

  passData = { old_password: '', new_password: '', confirm_password: '' };
  passMessage = '';
  isPassError = false;
  isSaving = false;

  constructor(
    private adminService: AdminService,
    private router: Router,
    private authService: AuthService
  ) { }

  ngOnInit() {
    this.loadUsers();
    this.loadProjects();
    this.loadMessages();
  }

  loadUsers() {
    this.adminService.getUsers().subscribe({
      next: (data: any[]) => {
        this.users = data;
        this.stats.freelancers = data.filter(u => u.user_type === 'freelancer').length;
        this.stats.clients = data.filter(u => u.user_type === 'client').length;
      },
      error: (err: any) => console.error('Error loading users:', err)
    });
  }

  loadProjects() {
    this.adminService.getProjects().subscribe({
      next: (data: any[]) => {
        this.projects = data;
        this.stats.projects = data.length;
      },
      error: (err: any) => console.error('Error loading projects:', err)
    });
  }

  loadMessages() {
    this.adminService.getMessages().subscribe({
      next: (data: any[]) => {
        this.messages = data;
        this.stats.messages = data.length;
        this.isLoading = false;
      },
      error: (err: any) => {
        console.error('Error loading messages:', err);
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
      error: (err: any) => {
        this.isSaving = false;
        this.passMessage = err.error?.old_password?.[0] || "Error changing password";
        this.isPassError = true;
      }
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/admin-login']);
  }
}