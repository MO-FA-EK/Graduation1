import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterModule, Router } from '@angular/router';
import { CommonModule, Location } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { FreelancerService, Freelancer } from '../../app/services/freelancer.service';
import { ProjectService } from '../../app/services/project.service';

@Component({
    selector: 'app-freelancer-profile',
    imports: [CommonModule, RouterModule, FormsModule],
    templateUrl: './freelancer-profile.component.html',
    styleUrls: ['./freelancer-profile.component.css']
})
export class FreelancerProfileComponent implements OnInit {
    freelancer: Freelancer | null = null;
    isLoading: boolean = true;
    userRating: number = 0;
    isRating: boolean = false;

    showHireModal: boolean = false;
    hireData = { title: '', description: '', amount: 50 };
    selectedFile: File | null = null;
    isHiring: boolean = false;

    constructor(
        private route: ActivatedRoute,
        private freelancerService: FreelancerService,
        private projectService: ProjectService,
        private location: Location,
        private router: Router
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
        this.freelancerService.getFreelancerById(id).subscribe({
            next: (data) => {
                this.freelancer = data;
                this.isLoading = false;
                this.freelancerService.incrementProfileViews(id).subscribe({
                    next: (newViewCount) => {
                        if (this.freelancer) {
                            this.freelancer.profileViews = newViewCount;
                        }
                    }
                });
            },
            error: () => this.isLoading = false
        });
    }

    openHireModal() {
        const token = localStorage.getItem('access_token');
        if (!token) {
            if (confirm('Please login to hire. Go to login?')) {
                this.router.navigate(['/login']);
            }
            return;
        }
        this.showHireModal = true;
    }

    closeHireModal() { this.showHireModal = false; }

    onFileSelected(event: any) {
        if (event.target.files && event.target.files.length > 0) {
            this.selectedFile = event.target.files[0];
        }
    }

    submitHireRequest() {
        if (!this.freelancer) return;
        if (!this.hireData.title || !this.hireData.description) {
            alert('Please fill in all fields.');
            return;
        }
        if (isNaN(Number(this.hireData.amount)) || Number(this.hireData.amount) <= 0) {
            alert('Please enter a valid amount.');
            return;
        }
        this.isHiring = true;

        const formData = new FormData();
        formData.append('title', this.hireData.title);
        formData.append('description', this.hireData.description);
        formData.append('amount', this.hireData.amount.toString());
        if (this.selectedFile) {
            formData.append('document', this.selectedFile);
        }

        this.projectService.createProject(this.freelancer.id, formData).subscribe({
            next: () => {
                alert('✅ Request sent! Check Dashboard.');
                this.isHiring = false;
                this.closeHireModal();
                this.router.navigate(['/dashboard']);
            },
            error: (err) => {
                alert(err.error?.error || 'Failed to send request.');
                this.isHiring = false;
            }
        });
    }

    rateFreelancer(stars: number): void {
        if (!this.freelancer || this.isRating) return;
        this.isRating = true;
        this.userRating = stars;
        this.freelancerService.rateFreelancer(this.freelancer.id, stars).subscribe({
            next: (res) => {
                if (this.freelancer) {
                    this.freelancer.rating = res.rating;
                    this.freelancer.totalRatings = res.totalRatings;
                }
                alert(`Rated ${stars} stars!`);
                this.isRating = false;
            },
            error: () => {
                alert('Login to rate!');
                this.isRating = false;
            }
        });
    }

    contactFreelancer(): void {
        if (!this.freelancer) return;
        this.freelancerService.incrementContactClicks(this.freelancer.id).subscribe();
        window.location.href = `mailto:${this.freelancer.email}`;
    }

    goBack(): void { this.location.back(); }
}
