import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AiService, ChatResponse } from '../../services/ai.service';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

interface ChatMessage {
    text: string;
    sender: 'user' | 'ai';
    timestamp: Date;
}

@Component({
    selector: 'app-ai-chat',
    standalone: true,
    imports: [CommonModule, FormsModule],
    templateUrl: './ai-chat.component.html',
    styleUrls: ['./ai-chat.component.css']
})
export class AiChatComponent implements OnInit {
    isOpen = false;
    messages: ChatMessage[] = [];
    userInput = '';
    isLoading = false;
    userRole = 'guest';

    @ViewChild('messagesContainer') private messagesContainer!: ElementRef;

    constructor(
        private aiService: AiService,
        private router: Router,
        private authService: AuthService
    ) { }

    ngOnInit(): void {
        const user = this.authService.getUser();
        if (user) {
            if (user.is_superuser) {
                this.userRole = 'admin';
            } else {
                this.userRole = user.user_type || 'auth_user';
            }
        }

        this.messages.push({
            text: "Hi! I'm your SoftwJob assistant. How can I help you navigate the platform today?",
            sender: 'ai',
            timestamp: new Date()
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        if (this.isOpen) {
            setTimeout(() => this.scrollToBottom(), 100);
        }
    }

    resetChat() {
        this.messages = [];
        this.messages.push({
            text: "Hi! I'm your SoftwJob assistant. How can I help you navigate the platform today?",
            sender: 'ai',
            timestamp: new Date()
        });
    }

    sendMessage() {
        if (!this.userInput.trim()) return;

        const userMsg = this.userInput;
        this.messages.push({ text: userMsg, sender: 'user', timestamp: new Date() });
        this.userInput = '';
        this.isLoading = true;
        this.scrollToBottom();

        const currentPage = this.router.url;

        this.aiService.sendMessage(userMsg, this.userRole, currentPage).subscribe({
            next: (response) => {
                this.messages.push({ text: response.reply, sender: 'ai', timestamp: new Date() });
                this.isLoading = false;
                this.scrollToBottom();
            },
            error: (err) => {
                this.messages.push({ text: "Sorry, I'm having trouble connecting right now.", sender: 'ai', timestamp: new Date() });
                this.isLoading = false;
                this.scrollToBottom();
            }
        });
    }

    scrollToBottom(): void {
        try {
            this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
        } catch (err) { }
    }
}
