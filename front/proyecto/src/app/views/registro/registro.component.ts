import { Component } from '@angular/core';
import {FormBuilder, FormGroup, Validators, ReactiveFormsModule} from '@angular/forms';
import {RouterLink} from '@angular/router';

@Component({
  selector: 'app-registro',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './registro.component.html',
  styleUrl: './registro.component.css'
})
export class RegistroComponent {
  registro_form: FormGroup;

  constructor(private fb: FormBuilder) {
    this.registro_form = this.fb.group({
      nombre: ['', [Validators.required, Validators.minLength(2)]],
      apellido: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      password_hash: ['', [Validators.required, Validators.minLength(8)]],
      confirmar_password: ['', [Validators.required, Validators.minLength(8)]]
    });
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

  on_submit () {
    if (this.registro_form.valid) {
      console.log('Formulario enviado:', this.registro_form.value);
    }
  }
}
