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

  feedbackMessage = '';
  isError = false;

  apiUrl = 'http://localhost:8000/api/contact/';

  sending = false;

  constructor(private http: HttpClient) { }

  sendMessage() {
    if (!this.name.trim() || !this.message.trim() || !this.email.trim()) {
      this.feedbackMessage = 'Name, email, and message are required!';
      this.isError = true;
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
          this.feedbackMessage = '✅ Message sent successfully to Support Team!';
          this.isError = false;
          this.name = '';
          this.email = '';
          this.message = '';
          this.sending = false;
        },
        error: (err) => {
          console.error(err);
          this.feedbackMessage = '❌ Failed to send message. Please try again later.';
          this.isError = true;
          this.sending = false;
        }
      });
  }
}
