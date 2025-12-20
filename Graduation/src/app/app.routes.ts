import { Routes } from '@angular/router';
import { HomepageComponent } from '../component/homepage/homepage.component';
import { ServicesComponent } from '../component/services/services.component';
import { ContactComponent } from '../component/contact/contact.component';
import { RegisterComponent } from '../component/register/register.component';
import { LoginComponent } from '../component/login/login.component';
import { DashboardComponent } from '../component/dashboard/dashboard.component';
import { AuthGuard } from './guards/auth.guard';
import { AdminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'homepage', pathMatch: 'full' },

  { path: 'homepage', component: HomepageComponent },
  { path: 'services', component: ServicesComponent },
  { path: 'contact', component: ContactComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },

  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },

  { path: 'admin/login', loadComponent: () => import('../component/admin-login/admin-login.component').then(m => m.AdminLoginComponent) },
  { path: 'admin', loadComponent: () => import('../component/admin/admin.component').then(m => m.AdminComponent), canActivate: [AdminGuard] },
  { path: 'freelancer/:id', loadComponent: () => import('../component/freelancer-profile/freelancer-profile.component').then(m => m.FreelancerProfileComponent) },

  { path: '**', redirectTo: 'homepage', pathMatch: 'full' },

];
