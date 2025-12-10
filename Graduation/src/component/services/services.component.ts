import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FreelancerService } from '../../app/services/freelancer.service';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-services',
  standalone: true,
  imports: [
  CommonModule,
  RouterModule,
  FormsModule     // ⭐ REQUIRED for ngModel
],

  templateUrl: './services.component.html',
  styleUrls: ['./services.component.css']
})
export class ServicesComponent implements OnInit {

  freelancers: any[] = [];
  filteredGroups: any[] = [];
  searchTerm: string = "";

  constructor(
  private freelancerService: FreelancerService,
  private route: ActivatedRoute
) {}


  ngOnInit(): void {
  this.route.queryParams.subscribe(params => {
    this.searchTerm = params['search'] || "";
    this.loadFreelancers(this.searchTerm);
  });
}


  loadFreelancers(search: string = ""): void {
  this.freelancerService.getFreelancers(search).subscribe({
    next: (data: any) => {
      this.freelancers = data;
      this.filteredGroups = this.groupByCategory(data);
    },
    error: (err: any) => {
      console.error(err);
    }
  });
}


  onSearch(): void {
  this.freelancerService.getFreelancers(this.searchTerm).subscribe({
    next: (data: any) => {
      this.freelancers = data;
      this.filteredGroups = this.groupByCategory(data);
    },
    error: (err: any) => {
      console.error(err);
    }
  });
}

clearSearch(): void {
  this.searchTerm = "";
  this.onSearch();
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
