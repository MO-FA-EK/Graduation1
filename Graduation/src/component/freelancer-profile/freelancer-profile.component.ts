import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { CommonModule, Location } from '@angular/common';
import { FreelancerService, Freelancer } from '../../app/services/freelancer.service';

@Component({
    selector: 'app-freelancer-profile',
    imports: [CommonModule, RouterModule],
    templateUrl: './freelancer-profile.component.html',
    styleUrls: ['./freelancer-profile.component.css']
})
export class FreelancerProfileComponent implements OnInit {
    freelancer: Freelancer | undefined;
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

    loadFreelancer(id: number) {
        this.freelancerService.getFreelancerById(id).subscribe(data => {
            this.freelancer = data;
            this.isLoading = false;

            if (this.freelancer) {
                this.freelancerService.incrementProfileViews(this.freelancer.id);
            }
        });
    }

    rateFreelancer(stars: number): void {
        if (!this.freelancer || this.isRating) return;

        this.isRating = true;
        this.userRating = stars;

        setTimeout(() => {
            if (this.freelancer) {

              const currentTotal = this.freelancer.rating * this.freelancer.totalRatings;
                const newTotalRatings = this.freelancer.totalRatings + 1;
                const newRating = (currentTotal + stars) / newTotalRatings;


                this.freelancer.rating = parseFloat(newRating.toFixed(1));
                this.freelancer.totalRatings = newTotalRatings;


                alert(`Thank you! You rated ${stars} stars.`);
                this.isRating = false;
            }
        }, 500);
    }

    contactFreelancer(): void {
        if (this.freelancer) {
            this.freelancerService.incrementContactClicks(this.freelancer.id);
            window.location.href = `mailto:${this.freelancer.email}?subject=Job Inquiry&body=Hi ${this.freelancer.username}...`;
        }
    }

    goBack(): void {
        this.location.back();
    }
}
