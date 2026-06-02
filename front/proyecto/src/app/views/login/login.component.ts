import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../service/AuthService/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {

  login_form: FormGroup;
  error_mensaje: string = '';
  cargando: boolean = false;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
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
    if (this.login_form.invalid) return;
    this.cargando = true;
    this.error_mensaje = '';

    const { email, password_hash } = this.login_form.value;
    this.authService.login(email, password_hash).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: (err) => {
        this.error_mensaje = err.error?.error || 'Error al iniciar sesión.';
        this.cargando = false;
      }
    });
  }
}
