import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule, AbstractControl, ValidationErrors } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { AuthService } from '../../service/AuthService/auth.service';

function passwordsIguales(group: AbstractControl): ValidationErrors | null {
  const pass = group.get('password_hash')?.value;
  const confirmarPass = group.get('confirmar_password')?.value;
  return pass === confirmarPass ? null : { noIguales: true };
}

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, CommonModule],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css'
})
export class RegistroComponent {
  registro_form: FormGroup;
  error_mensaje: string = '';
  cargando: boolean = false;

  constructor(private fb: FormBuilder, private authService: AuthService, private router: Router) {
    this.registro_form = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      apellido: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password_hash: ['', [Validators.required, Validators.minLength(8)]],
      confirmar_password: ['', [Validators.required, Validators.minLength(8)]]
    }, { validators: passwordsIguales });
  }

  get nombre() {
    return this.registro_form.get('nombre');
  }
  get apellido() {
    return this.registro_form.get('apellido');
  }
  get email() {
    return this.registro_form.get('email');
  }
  get password_hash() {
    return this.registro_form.get('password_hash');
  }
  get confirmar_password() {
    return this.registro_form.get('confirmar_password');
  }

  on_submit() {
    if (this.registro_form.invalid) return;
    this.cargando = true;
    this.error_mensaje = '';

    const { nombre, apellido, email, password_hash, confirmar_password } = this.registro_form.value;
    this.authService.registro({
      first_name: nombre,
      last_name: apellido,
      email,
      password: password_hash,
      confirmar_password
    }).subscribe({
      next: () => this.router.navigate(['/dashboard']),
      error: (err) => {
        const errores = err.error;
        this.error_mensaje = errores?.email?.[0] || errores?.password?.[0] || errores?.detail || 'Error al registrarse.';
        this.cargando = false;
      }
    });
  }
}
