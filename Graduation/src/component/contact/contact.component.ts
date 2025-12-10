import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-contact',
  imports: [CommonModule, FormsModule],
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent {
  name = '';
  email = '';
  message = '';

  // The real link to the backend
  apiUrl = 'http://localhost:8000/api/contact/';

  sending = false;

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.name.trim() || !this.message.trim()) {
      alert('Name and message are required!');
      return;
    }

    this.sending = true;

    this.http.post(this.apiUrl, {
      name: this.name,
      email: this.email,
      message: this.message
    })
    .subscribe({
      next: (res: any) => {
        alert('✅ Message sent successfully to Support Team!');
        this.name = '';
        this.email = '';
        this.message = '';
        this.sending = false;
      },
      error: (err) => {
        console.error(err);
        alert('❌ Failed to send message. Please try again later.');
        this.sending = false;
      }
    });
  }
}
