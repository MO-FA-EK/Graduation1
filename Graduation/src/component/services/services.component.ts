import { Component, OnInit } from '@angular/core';
import { RouterModule, ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FreelancerService, Freelancer } from '../../app/services/freelancer.service';

@Component({
  selector: 'app-services',
  imports: [RouterModule, CommonModule, FormsModule],
  templateUrl: './services.component.html',
  styleUrls: ['./services.component.css']
})
export class ServicesComponent implements OnInit {

  freelancers: Freelancer[] = [];
  groupedFreelancers: { category: string, freelancers: Freelancer[] }[] = [];
  filteredGroups: { category: string, freelancers: Freelancer[] }[] = [];
  searchTerm: string = '';

  constructor(
    private freelancerService: FreelancerService,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {

    this.route.queryParams.subscribe(params => {
      this.searchTerm = params['search'] || '';
      this.loadFreelancers();
    });
  }

  loadFreelancers() {
    this.freelancerService.getFreelancers().subscribe(data => {
      this.freelancers = data;
      this.groupFreelancers();
      this.filterServices();
    });
  }

  groupFreelancers() {
    const groups: { [key: string]: Freelancer[] } = {};
    this.freelancers.forEach(f => {
      const cat = f.category || 'General';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(f);
    });

    this.groupedFreelancers = Object.keys(groups).map(category => ({
      category,
      freelancers: groups[category]
    }));
  }

  filterServices() {
    if (!this.searchTerm) {
      this.filteredGroups = this.groupedFreelancers;
      return;
    }

    const term = this.searchTerm.toLowerCase().trim();

    this.filteredGroups = this.groupedFreelancers
      .map(group => {

        const isCategoryMatch = group.category.toLowerCase().includes(term);

        if (isCategoryMatch) {
          return group;
        }

        const matchingFreelancers = group.freelancers.filter(f =>
          f.username.toLowerCase().includes(term) ||
          f.description.toLowerCase().includes(term) ||
          f.skills.some(skill => skill.toLowerCase().includes(term))
        );

        return { category: group.category, freelancers: matchingFreelancers };
      })

      .filter(group => group.freelancers.length > 0);
  }

  trackFreelancer(index: number, freelancer: Freelancer) {
    return freelancer.id;
  }
}
