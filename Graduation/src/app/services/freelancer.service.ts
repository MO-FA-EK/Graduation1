import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

export interface Freelancer {
    id: number;
    username: string;
    email: string;
    category: string;
    description: string;
    skills: string[];
    portfolio?: string;
    imageUrl?: string;
    rating: number;
    totalRatings: number;
    profileViews: number;
    contactClicks: number;
}

@Injectable({
    providedIn: 'root'
})
export class FreelancerService {
    private storageKey = 'mock_freelancers';

    // بيانات وهمية ابتدائية (تظهر أول مرة فقط)
    private initialFreelancers: Freelancer[] = [
        {
            id: 1,
            username: 'John Doe',
            email: 'john@example.com',
            category: 'Frontend Developer',
            description: 'Expert in Angular and React.',
            skills: ['Angular', 'React', 'TypeScript', 'CSS'],
            portfolio: 'https://john.example.com',
            imageUrl: 'assets/img/user.png',
            rating: 4.8,
            totalRatings: 15,
            profileViews: 120,
            contactClicks: 30
        },
        {
            id: 2,
            username: 'Jane Smith',
            email: 'jane@example.com',
            category: 'Backend Developer',
            description: 'Specialist in Node.js and Python.',
            skills: ['Node.js', 'Python', 'MongoDB', 'SQL'],
            imageUrl: 'assets/img/user.png',
            rating: 4.9,
            totalRatings: 20,
            profileViews: 200,
            contactClicks: 45
        }
    ];

    constructor() {
        // عند تشغيل السيرفس، نتحقق هل هناك بيانات محفوظة؟ إذا لا، نحفظ البيانات الابتدائية
        if (!localStorage.getItem(this.storageKey)) {
            this.saveToStorage(this.initialFreelancers);
        }
    }

    // جلب القائمة من LocalStorage
    getFreelancers(): Observable<Freelancer[]> {
        const data = localStorage.getItem(this.storageKey);
        const freelancers = data ? JSON.parse(data) : [];
        return of(freelancers);
    }

    getFreelancerById(id: number): Observable<Freelancer | undefined> {
        const freelancers = this.getAllFromStorage();
        const freelancer = freelancers.find(f => f.id === id);
        return of(freelancer);
    }

    // إضافة فريلانسر جديد (يستخدم عند التسجيل)
    addFreelancer(newFreelancer: any): void {
        const freelancers = this.getAllFromStorage();

        const id = freelancers.length > 0 ? Math.max(...freelancers.map(f => f.id)) + 1 : 1;

        const freelancer: Freelancer = {
            id: id,
            username: newFreelancer.username,
            email: newFreelancer.email,
            category: newFreelancer.category,
            description: newFreelancer.description,
            // تحويل النص إلى مصفوفة إذا كان نصاً
            skills: typeof newFreelancer.skills === 'string'
                    ? newFreelancer.skills.split(',').map((s: string) => s.trim())
                    : newFreelancer.skills || [],
            portfolio: newFreelancer.portfolio,
            imageUrl: newFreelancer.imageUrl || 'assets/img/user.png',
            rating: 0,
            totalRatings: 0,
            profileViews: 0,
            contactClicks: 0
        };

        freelancers.push(freelancer);
        this.saveToStorage(freelancers);
    }

    // دوال مساعدة خاصة
    private getAllFromStorage(): Freelancer[] {
        const data = localStorage.getItem(this.storageKey);
        return data ? JSON.parse(data) : [];
    }

    private saveToStorage(data: Freelancer[]): void {
        localStorage.setItem(this.storageKey, JSON.stringify(data));
    }

    incrementProfileViews(id: number): void {
        const freelancers = this.getAllFromStorage();
        const index = freelancers.findIndex(f => f.id === id);
        if (index !== -1) {
            freelancers[index].profileViews++;
            this.saveToStorage(freelancers);
        }
    }

    incrementContactClicks(id: number): void {
        const freelancers = this.getAllFromStorage();
        const index = freelancers.findIndex(f => f.id === id);
        if (index !== -1) {
            freelancers[index].contactClicks++;
            this.saveToStorage(freelancers);
        }
    }
}
