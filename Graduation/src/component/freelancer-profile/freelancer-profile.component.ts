import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CommonModule, Location } from '@angular/common';
import { FreelancerService, Freelancer } from '../../app/services/freelancer.service';

@Component({
  selector: 'app-freelancer-profile',
  templateUrl: './freelancer-profile.component.html',
  styleUrls: ['./freelancer-profile.component.css'],
  imports: [CommonModule, RouterModule]
})
export class FreelancerProfileComponent implements OnInit {

  freelancer: Freelancer | null = null;
  isLoading = true;
  userRating = 0;
  isRating = false;

  constructor(
    private route: ActivatedRoute,
    private freelancerService: FreelancerService,
    private location: Location
  ) {}

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) this.loadFreelancer(id);
  }

  loadFreelancer(id: number): void {
    this.freelancerService.getFreelancerById(id).subscribe(data => {
      this.freelancer = data;
      this.isLoading = false;

      this.freelancerService.incrementProfileViews(id).subscribe(views => {
        if (this.freelancer) this.freelancer.profileViews = views;
      });
    });
  }

  rateFreelancer(stars: number): void {
    if (!this.freelancer || this.isRating) return;

    this.isRating = true;
    this.userRating = stars;

    this.freelancerService.rateFreelancer(this.freelancer.id, stars).subscribe({
      next: (res) => {

        /** FIXED: Use correct backend field names */
        if (this.freelancer) {
          this.freelancer.rating = res.average_rating;
          this.freelancer.totalRatings = res.total_ratings;
        }

        /** FIXED: Reload the freelancer to get fresh average */
        this.loadFreelancer(this.freelancer!.id);

        this.isRating = false;
      },
      error: () => {
        alert("Failed to save rating.");
        this.isRating = false;
      }
    });
  }

  contactFreelancer(): void {
    if (!this.freelancer) return;
    this.freelancerService.incrementContactClicks(this.freelancer.id).subscribe(clicks => {
      if (this.freelancer) this.freelancer.contactClicks = clicks;
    });
    window.location.href = `mailto:${this.freelancer.email}`;
  }

  goBack(): void {
    this.location.back();
  }
}
