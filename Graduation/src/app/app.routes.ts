// import { Routes } from '@angular/router';
// import { HomepageComponent } from '../component/homepage/homepage.component';
// import { ServicesComponent } from '../component/services/services.component';
// import { ContactComponent } from '../component/contact/contact.component';
// import { RegisterComponent } from '../component/register/register.component';
// import { LoginComponent } from '../component/login/login.component';
// import { DashboardComponent } from '../component/dashboard/dashboard.component';
// import { AuthGuard } from './guards/auth.guard';
// import {  } from './guards/auth.guard';
// export const routes: Routes = [

// {
// path: '',
// component: HomepageComponent,


// },


// {
// path: 'homepage',
// component: HomepageComponent

// },

// {
// path: 'services',
// component: ServicesComponent

// },


// {
// path: 'contact',
// component: ContactComponent

// },

// {
// path: 'register',
// component: RegisterComponent

// },

// {
// path: 'login',
// component: LoginComponent

// },

// {
// path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard]


// },

// {
// path: '**', redirectTo: '', pathMatch: 'full'

// },



// ];










import { Routes } from '@angular/router';
import { HomepageComponent } from '../component/homepage/homepage.component';
import { ServicesComponent } from '../component/services/services.component';
import { ContactComponent } from '../component/contact/contact.component';
import { RegisterComponent } from '../component/register/register.component';
import { LoginComponent } from '../component/login/login.component';
import { DashboardComponent } from '../component/dashboard/dashboard.component';
import { AuthGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: 'homepage', pathMatch: 'full' },

  { path: 'homepage', component: HomepageComponent },
  { path: 'services', component: ServicesComponent },
  { path: 'contact', component: ContactComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'login', component: LoginComponent },

  // أهم شيء هنا
  { path: 'dashboard', component: DashboardComponent, canActivate: [AuthGuard] },
  // canActivate: [AuthGuard]

  { path: 'freelancer/:id', loadComponent: () => import('../component/freelancer-profile/freelancer-profile.component').then(m => m.FreelancerProfileComponent) },

  { path: '**', redirectTo: 'homepage', pathMatch: 'full' },

  {
  path: 'services',
  component: ServicesComponent
}

];
