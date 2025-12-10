import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [
    CommonModule,   // ← REQUIRED
    RouterLink,     // ← For routerLink
    FormsModule     // ← For ngModel
  ],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent {

  searchTerm: string = '';

  constructor(private router: Router) {}

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
