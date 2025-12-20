import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
    providedIn: 'root'
})
export class GithubService {
    private apiUrl = 'https://api.github.com/repos';

    constructor(private http: HttpClient) { }

    getCommits(repoUrl: string): Observable<any[]> {
        const repoPath = this.extractRepoPath(repoUrl);
        if (!repoPath) {
            return of([]);
        }

        const url = `${this.apiUrl}/${repoPath}/commits`;
        return this.http.get<any[]>(url).pipe(
            map(commits => commits.slice(0, 10)), 
            catchError(error => {
                console.error('Error fetching commits:', error);
                return of([]);
            })
        );
    }

    private extractRepoPath(url: string): string | null {
        try {
            const cleanUrl = url.replace(/\/$/, ''); 
            const parts = cleanUrl.split('github.com/');
            if (parts.length === 2) {
                return parts[1];
            }
        } catch (e) {
            console.error('Invalid GitHub URL:', url);
        }
        return null;
    }
}
