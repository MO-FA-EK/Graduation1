import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../app/services/auth.service';

@Component({
  selector: 'app-header',
  imports: [
    CommonModule,
    RouterLink,
    FormsModule
  ],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  searchTerm: string = '';

  constructor(private router: Router, private authService: AuthService) { }

  get isAdmin(): boolean {
    const user = this.authService.getUser();
    return user?.is_superuser === true;
  }

  get isLoggedIn(): boolean {
    return this.authService.isLoggedIn();
  }

  onSearch() {
    if (this.searchTerm.trim()) {
      this.router.navigate(['/services'], {
        queryParams: { search: this.searchTerm.trim() }
      });
    } else {
      this.router.navigate(['/services']);
    }
  }
}
