import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FreelancerService } from '../../app/services/freelancer.service';

@Component({
  selector: 'app-services',
  standalone: true,
  imports: [
    CommonModule,   // ← gives you *ngIf, *ngFor, slice pipe
    RouterModule    // ← gives you routerLink
  ],
  templateUrl: './services.component.html',
  styleUrls: ['./services.component.css']
})
export class ServicesComponent implements OnInit {

  freelancers: any[] = [];
  filteredGroups: any[] = [];
  searchTerm: string = "";

  constructor(private freelancerService: FreelancerService) {}

  ngOnInit(): void {
    this.loadFreelancers();
  }

  loadFreelancers(): void {
    this.freelancerService.getFreelancers().subscribe({
      next: (data: any) => {
        this.freelancers = data;
        this.filteredGroups = this.groupByCategory(data);
      },
      error: (err: any) => {
        console.error(err);
      }
    });
  }

  groupByCategory(list: any[]) {
    const categories: any = {};

    list.forEach(user => {
      if (!categories[user.category]) {
        categories[user.category] = [];
      }
      categories[user.category].push(user);
    });

    return Object.keys(categories).map(category => ({
      category,
      freelancers: categories[category]
    }));
  }

  trackFreelancer(index: number, item: any) {
    return item.id;
  }
}
