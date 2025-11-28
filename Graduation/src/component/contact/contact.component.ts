import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { catchError, of } from 'rxjs';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent {
  name = '';
  email = ''; // optional
  message = '';
  apiUrl = 'https://your-backend-api/contact'; // رابط الـ backend الخاص بالرسائل

  sending = false;

  constructor(private http: HttpClient) {}

  sendMessage() {
    if (!this.name.trim() || !this.message.trim()) {
      alert('Name and message are required!');
      return;
    }

    this.sending = true;

    this.http.post(this.apiUrl, { name: this.name, email: this.email, message: this.message })
      .pipe(
        catchError(err => {
          console.error(err);
          alert('Failed to send message.');
          this.sending = false;
          return of(null);
        })
      )
      .subscribe(res => {
        if (res !== null) {
          alert('Message sent successfully!');
          this.name = this.email = this.message = '';
        }
        this.sending = false;
      });
  }
}
