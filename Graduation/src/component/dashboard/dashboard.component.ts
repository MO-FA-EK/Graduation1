import { Component, OnInit, ViewChild } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { AuthService, User } from '../../app/services/auth.service';
import { ProjectService, Project } from '../../app/services/project.service';
import { StripeService, StripeCardComponent } from 'ngx-stripe';
import { StripeCardElementOptions, StripeElementsOptions } from '@stripe/stripe-js';

@Component({
  selector: 'app-dashboard',
  imports: [FormsModule, CommonModule, RouterModule, StripeCardComponent],
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

  passData = { old_password: '', new_password: '', confirm_password: '' };
  passMessage = '';
  isPassError = false;

  showPaymentModal = false;
  selectedProjectForPayment: Project | null = null;
  isProcessingPayment = false;

  @ViewChild(StripeCardComponent) card!: StripeCardComponent;

  cardOptions: StripeCardElementOptions = {
    style: {
      base: {
        iconColor: '#666EE8',
        color: '#31325F',
        fontWeight: '300',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSize: '18px',
        '::placeholder': { color: '#CFD7E0' }
      }
    }
  };
  elementsOptions: StripeElementsOptions = { locale: 'en' };

  constructor(
    private authService: AuthService,
    private projectService: ProjectService,
    private router: Router,
    private stripeService: StripeService
  ) { }

  ngOnInit() { this.loadProfile(); }

  loadProfile() {
    this.authService.getUserProfile().subscribe({
      next: (user) => {
        if (user) {
          this.profile = user;

          this.isClient = (this.profile.user_type?.toLowerCase() === 'client');
          this.loadProjects();
        } else {
          this.isLoading = false;
        }
      },
      error: () => {
        this.isLoading = false;
        this.router.navigate(['/login']);
      }
    });
  }

  loadProjects() {
    this.projectService.getMyProjects().subscribe({
      next: (res: any) => {
        console.log('Projects Data:', res);

        this.hiredProjects = res.hired_projects || [];
        this.workProjects = res.work_projects || [];

        this.isLoading = false;
      },
      error: (err) => {
        console.error('Failed to load projects:', err);

        this.hiredProjects = [];
        this.workProjects = [];
        this.isLoading = false;
      }
    });
  }

  openPaymentModal(project: Project) {
    this.selectedProjectForPayment = project;
    this.showPaymentModal = true;
  }

  closePaymentModal() {
    this.showPaymentModal = false;
    this.selectedProjectForPayment = null;
  }

  payNow() {
    if (!this.selectedProjectForPayment) return;
    this.isProcessingPayment = true;

    this.projectService.createPaymentIntent(this.selectedProjectForPayment.id).subscribe({
      next: (res) => {
        const clientSecret = res.clientSecret;
        this.stripeService.confirmCardPayment(clientSecret, {
          payment_method: {
            card: this.card.element,
            billing_details: { name: this.profile?.username }
          }
        }).subscribe((result) => {
          if (result.error) {
            alert('Payment Failed: ' + result.error.message);
            this.isProcessingPayment = false;
          } else {
            if (result.paymentIntent.status === 'succeeded') {
              this.projectService.confirmPaymentOnServer(result.paymentIntent.id).subscribe(() => {
                alert('✅ Payment Successful! Project Started.');
                this.closePaymentModal();
                this.isProcessingPayment = false;
                this.loadProjects();
              });
            }
          }
        });
      },
      error: (err) => {
        alert('Error: ' + (err.error?.error || 'Payment Init Failed'));
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

  saveProfile() {
    if (!this.profile) return;
    this.isSaving = true;
    this.authService.updateUser(this.profile).subscribe({
      next: (user) => {
        this.isSaving = false;
        this.profile = user;
        alert('Profile saved!');
      },
      error: () => {
        this.isSaving = false;
        alert('Save failed.');
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
        error: () => { this.isSaving = false; this.passMessage = "Error changing password"; }
    });
  }

  setTab(tab: string) { this.activeTab = tab; this.isSidebarOpen = false; }
  toggleSidebar() { this.isSidebarOpen = !this.isSidebarOpen; }
  logout() { if(confirm('Logout?')) this.authService.logout(); }
}
