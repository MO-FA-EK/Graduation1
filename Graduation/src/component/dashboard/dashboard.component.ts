import { Component, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule, ActivatedRoute } from '@angular/router';
import { AuthService, User } from '../../app/services/auth.service';
import { ProjectService, Project } from '../../app/services/project.service';
import { GithubService } from '../../app/services/github.service';
import { FilterStatusPipe } from '../../app/pipes/filter-status.pipe';

import { StripeService, StripePaymentElementComponent, NgxStripeModule } from 'ngx-stripe';
import { StripeElementsOptions, StripePaymentElementOptions } from '@stripe/stripe-js';

@Component({
  selector: 'app-dashboard',
  imports: [
    FormsModule,
    CommonModule,
    RouterModule,
    FilterStatusPipe,
    NgxStripeModule,
    StripePaymentElementComponent
  ],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  activeTab: string = 'projects';
  isLoading: boolean = true;
  isSaving: boolean = false;
  isSidebarOpen: boolean = false;

  profile: User | null = null;
  isClient: boolean = false;

  hiredProjects: Project[] = [];
  workProjects: Project[] = [];
  completedProjects: Project[] = [];

  passData = { old_password: '', new_password: '', confirm_password: '' };
  passMessage = '';
  isPassError = false;

  showPaymentModal = false;
  selectedProjectForPayment: Project | null = null;
  isProcessingPayment = false;

  showCommitsModal = false;
  commits: any[] = [];
  selectedProjectForCommits: Project | null = null;
  isLoadingCommits = false;

  showStatsModal = false;
  statsData: any = null;
  selectedProjectForStats: any = null;
  isLoadingStats = false;

  elementsOptions: StripeElementsOptions = {
    locale: 'en',
    appearance: { theme: 'stripe' }
  };

  paymentElementOptions: StripePaymentElementOptions = {
    layout: { type: 'tabs' }
  };

  @ViewChild(StripePaymentElementComponent) paymentElement!: StripePaymentElementComponent;

  constructor(
    private authService: AuthService,
    private projectService: ProjectService,
    private router: Router,
    private stripeService: StripeService,
    private githubService: GithubService
  ) { }

  ngOnInit() {
    this.loadProfile();
  }

  loadProfile() {
    this.authService.getUserProfile().subscribe({
      next: (res: User | null) => {
        if (res) {
          if (res.is_superuser || res.user_type === 'admin') {
            this.router.navigate(['/admin']);
            return;
          }
          this.profile = res;
          this.isClient = !res.category;
          this.loadProjects();
        } else {
          this.router.navigate(['/login']);
        }
      },
      error: () => {
        this.router.navigate(['/login']);
      }
    });
  }

  loadProjects() {
    this.isLoading = true;
    this.projectService.getMyProjects().subscribe({
      next: (res: any) => {
        this.hiredProjects = res.hired_projects || [];

        const allWork = res.work_projects || [];
        this.workProjects = allWork.filter((p: Project) => p.status !== 'completed' && p.status !== 'rejected');
        this.completedProjects = allWork.filter((p: Project) => p.status === 'completed');

        this.isLoading = false;
      },
      error: () => {
        this.hiredProjects = [];
        this.workProjects = [];
        this.completedProjects = [];
        this.isLoading = false;
      }
    });
  }

  openPaymentModal(project: Project) {
    this.selectedProjectForPayment = project;
    this.isProcessingPayment = true;

    this.projectService.createPaymentIntent(project.id).subscribe({
      next: (res) => {
        this.elementsOptions = {
          clientSecret: res.clientSecret,
          appearance: { theme: 'stripe' }
        };
        this.showPaymentModal = true;
        this.isProcessingPayment = false;
      },
      error: (err) => {
        alert('Failed to initialize payment');
        this.isProcessingPayment = false;
      }
    });
  }

  closePaymentModal() {
    this.showPaymentModal = false;
    this.selectedProjectForPayment = null;
  }

  payNow() {
    if (this.isProcessingPayment) return;
    this.isProcessingPayment = true;

    const billingDetails: any = {};
    if (this.profile?.username) billingDetails.name = this.profile.username;
    if (this.profile?.email) billingDetails.email = this.profile.email;

    this.stripeService.confirmPayment({
      elements: this.paymentElement.elements,
      confirmParams: {
        return_url: window.location.href,
        payment_method_data: {
          billing_details: billingDetails
        }
      },
      redirect: 'if_required'
    }).subscribe({
      next: (result) => {
        this.isProcessingPayment = false;
        if (result.error) {
          alert('Payment Validation Failed: ' + result.error.message);
        } else if (result.paymentIntent && result.paymentIntent.status === 'succeeded') {
          alert('✅ Payment Successful!');
          const projectToUpdate = this.selectedProjectForPayment;
          this.closePaymentModal();

          if (projectToUpdate) {
            this.projectService.markProjectAsPaid(projectToUpdate.id).subscribe(() => {
              this.loadProjects();
            });
          }
        }
      },
      error: (err) => {
        console.error('Payment Error:', err);
        alert('Error processing payment: ' + (err.message || JSON.stringify(err)));
        this.isProcessingPayment = false;
      }
    });
  }

  updateProject(project: Project) {
    const updateData = { github_link: project.github_link, status: project.status };
    this.projectService.updateProject(project.id, updateData).subscribe({
      next: () => alert('Updated successfully!'),
      error: () => alert('Update failed.')
    });
  }

  acceptProject(project: Project) {
    if (!confirm('Accept this project?')) return;
    this.projectService.acceptProject(project.id).subscribe({
      next: () => {
        alert('Project Accepted!');
        this.loadProjects();
      },
      error: (err: any) => alert(err.error?.error || 'Error accepting project')
    });
  }

  rejectProject(project: Project) {
    if (!confirm('Reject this project?')) return;
    this.projectService.rejectProject(project.id).subscribe({
      next: () => {
        alert('Project Rejected');
        this.loadProjects();
      },
      error: (err: any) => alert(err.error?.error || 'Error rejecting project')
    });
  }

  completeProject(project: Project) {
    if (!confirm('Mark this project as COMPLETED?')) return;
    this.projectService.completeProject(project.id).subscribe({
      next: () => {
        alert('Project Completed! Great job!');
        this.loadProjects();
      },
      error: (err: any) => alert(err.error?.error || 'Error completing project')
    });
  }

  saveProfile() {
    if (!this.profile) return;
    this.isSaving = true;
    this.authService.updateUser(this.profile).subscribe({
      next: (user) => {
        this.isSaving = false;
        this.profile = user;
        alert('Profile saved!');
      },
      error: (err) => {
        console.error('Save failed', err);
        this.isSaving = false;
        alert('Save failed: ' + (err.error?.detail || err.message || JSON.stringify(err)));
      }
    });
  }

  changePasswordSubmit() {
    this.passMessage = '';
    this.isPassError = false;
    if (this.passData.new_password !== this.passData.confirm_password) {
      this.passMessage = "Passwords do not match"; this.isPassError = true; return;
    }
    this.isSaving = true;
    this.authService.changePassword({
      old_password: this.passData.old_password,
      new_password: this.passData.new_password
    }).subscribe({
      next: () => { this.isSaving = false; this.passMessage = "Changed!"; },
      error: (err) => {
        this.isSaving = false;
        console.error(err);
        if (err.error?.old_password) {
          this.passMessage = err.error.old_password[0];
        } else if (err.error?.new_password) {
          this.passMessage = err.error.new_password[0];
        } else {
          this.passMessage = err.error?.detail || "Error changing password";
        }
        this.isPassError = true;
      }
    });
  }

  viewCommits(project: Project) {
    if (!project.github_link) {
      alert('No GitHub link provided for this project.');
      return;
    }
    this.selectedProjectForCommits = project;
    this.showCommitsModal = true;
    this.isLoadingCommits = true;
    this.commits = [];

    this.githubService.getCommits(project.github_link).subscribe({
      next: (data: any[]) => {
        this.commits = data;
        this.isLoadingCommits = false;
      },
      error: () => {
        this.isLoadingCommits = false;
        alert('Failed to load commits. Make sure the repo is public.');
      }
    });
  }

  closeCommitsModal() {
    this.showCommitsModal = false;
    this.selectedProjectForCommits = null;
  }

  viewStats(project: any) {
    this.selectedProjectForStats = project;
    this.showStatsModal = true;
    this.isLoadingStats = true;
    this.statsData = null;

    this.projectService.getProjectStats(project.id).subscribe({
      next: (data) => {
        this.statsData = data;
        this.isLoadingStats = false;
      },
      error: (err) => {
        console.error(err);
        this.isLoadingStats = false;
        alert('Could not fetch stats. Make sure a GitHub repo is linked.');
        this.showStatsModal = false;
      }
    });
  }

  closeStatsModal() {
    this.showStatsModal = false;
    this.statsData = null;
    this.selectedProjectForStats = null;
  }

  setTab(tab: string) { this.activeTab = tab; this.isSidebarOpen = false; }
  toggleSidebar() { this.isSidebarOpen = !this.isSidebarOpen; }
  logout() { if (confirm('Logout?')) this.authService.logout(); }
}