import { Component } from '@angular/core';
import {FormBuilder, FormGroup, Validators, ReactiveFormsModule} from '@angular/forms';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  login_form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.login_form = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password_hash: ['', [Validators.required, Validators.minLength(8)]]
    });
  }

  get email() {
    return this.login_form.get('email');
  }

  get password_hash() {
    return this.login_form.get('password_hash');
  }

  on_submit() {
    if (this.login_form.valid) {
      console.log('Formulario enviado:', this.login_form.value);
    }
  }
}
