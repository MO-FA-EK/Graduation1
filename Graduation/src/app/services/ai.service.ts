import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface ChatRequest {
    message: string;
    role?: string;
    current_page?: string;
}

export interface ChatResponse {
    reply: string;
    error?: string;
}

@Injectable({
    providedIn: 'root'
})
export class AiService {
    private apiUrl = 'http://localhost:8000/api/ai/chat/';

    constructor(private http: HttpClient) { }

    sendMessage(message: string, role: string = 'guest', currentPage: string = '/'): Observable<ChatResponse> {
        const payload: ChatRequest = {
            message,
            role,
            current_page: currentPage
        };
        return this.http.post<ChatResponse>(this.apiUrl, payload);
    }
}
