import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CommonModule, Location } from '@angular/common';
import { FreelancerService, Freelancer } from '../../app/services/freelancer.service';

@Component({
    selector: 'app-freelancer-profile',
    standalone: true,
    imports: [CommonModule, RouterModule],
    templateUrl: './freelancer-profile.component.html',
    styleUrls: ['./freelancer-profile.component.css']
})
export class FreelancerProfileComponent implements OnInit {
    freelancer: Freelancer | null = null;
    isLoading: boolean = true;
    userRating: number = 0;
    isRating: boolean = false;

    constructor(
        private route: ActivatedRoute,
        private freelancerService: FreelancerService,
        private location: Location
    ) { }

    ngOnInit(): void {
        const id = Number(this.route.snapshot.paramMap.get('id'));
        if (id) {
            this.loadFreelancer(id);
        } else {
            this.isLoading = false;
        }
    }

    loadFreelancer(id: number): void {
        this.freelancerService.getFreelancerById(id).subscribe(data => {
            this.freelancer = data;
            this.isLoading = false;

// Increase views
            this.freelancerService.incrementProfileViews(id).subscribe(newViews => {
                if (this.freelancer) this.freelancer.profileViews = newViews;
            });
        });
    }

 // Real Evaluation Function

    rateFreelancer(stars: number): void {
        if (!this.freelancer || this.isRating) return;

        this.isRating = true;
        this.userRating = stars;


       // Connect to the server
        this.freelancerService.rateFreelancer(this.freelancer.id, stars).subscribe({
            next: (res) => {
                if (this.freelancer) {



  // Update numbers based on server response
                  this.freelancer.rating = res.rating;
                    this.freelancer.totalRatings = res.totalRatings || (this.freelancer.totalRatings + 1);
                }
                alert(`Thank you! You rated ${stars} stars.`);
                this.isRating = false;
            },
            error: (err) => {
                console.error(err);
                alert('Failed to save rating. Please try again.');
                this.isRating = false;
            }
        });
    }

    contactFreelancer(): void {
        if (!this.freelancer) return;
        this.freelancerService.incrementContactClicks(this.freelancer.id).subscribe(newClicks => {
            if (this.freelancer) this.freelancer.contactClicks = newClicks;
        });
        window.location.href = `mailto:${this.freelancer.email}`;
    }

    goBack(): void {
        this.location.back();
    }
}
