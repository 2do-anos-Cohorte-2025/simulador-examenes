import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../service/admin.service';
import { AuthService } from '../../service/AuthService/auth.service'; 

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrl: './admin-dashboard.component.css'
})
export class AdminDashboardComponent implements OnInit {

  seccionActiva: 'usuarios' | 'examenes' = 'usuarios';

  usuarios: any[] = [];
  examenes: any[] = [];

  mostrarModal = false;
  modoModal: 'crear' | 'editar' = 'crear';
  itemEditando: any = null;

  form: any = {};

  
  constructor(
    private api: AdminService,
    private authService: AuthService 
  ) {}

  ngOnInit() {
    this.cargarTodo();
  }

  cargarTodo() {
    this.api.getUsuarios().subscribe(data => this.usuarios = data);
    this.api.getExamenes().subscribe(data => this.examenes = data);
  }

  cambiarSeccion(seccion: 'usuarios' | 'examenes') {
    this.seccionActiva = seccion;
    this.cerrarModal();
  }

  abrirModalCrear() {
    this.modoModal = 'crear';
    this.form = {
      rol: 'estudiante' 
    };
    this.mostrarModal = true;
  }

  abrirModalEditar(item: any) {
    this.modoModal = 'editar';
    this.itemEditando = item;
    this.form = { ...item };
    this.mostrarModal = true;
  }

  cerrarModal() {
    this.mostrarModal = false;
    this.itemEditando = null;
    this.form = {};
  }

  guardar() {
    if (this.modoModal === 'crear') {
      this.crear();
    } else {
      this.editar();
    }
  }

  crear() {
    if (this.seccionActiva === 'usuarios') {
      
      if (!this.form.email) {
        alert('Por favor, ingresa un correo electrónico.');
        return;
      }

      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailRegex.test(this.form.email)) {
        alert('El formato del correo electrónico no es válido (ejemplo: usuario@email.com).');
        return;
      }

      
      if (!this.form.password || !this.form.confirmPassword) {
        alert('Por favor, completa los campos de contraseña.');
        return;
      }

      
      if (this.form.password.length < 8) {
        alert('La contraseña debe contener al menos 8 caracteres.');
        return;
      }

      
      if (this.form.password !== this.form.confirmPassword) {
        alert('Las contraseñas no coinciden. Revisa e intenta de nuevo.');
        return;
      }

      
      const payloadRegistro = {
        username: this.form.email,
        email: this.form.email,
        first_name: this.form.first_name || '',
        last_name: this.form.last_name || '',
        password: this.form.password,                    
        confirmar_password: this.form.confirmPassword,     
        rol: this.form.rol || 'estudiante'
      };

      
      this.authService.registro(payloadRegistro).subscribe({
        next: () => { 
          this.cargarTodo(); 
          this.cerrarModal(); 
          alert('¡Usuario creado con éxito y contraseña encriptada!');
        },
        error: (err) => {
          console.error('Error al registrar mediante AuthService:', err);
          alert('No se pudo crear el usuario. Revisa que el email no esté repetido.');
        }
      });

    } else if (this.seccionActiva === 'examenes') {
      if (this.form.titulo && !this.form.slug) {
        this.form.slug = this.form.titulo
          .toLowerCase()
          .trim()
          .replace(/[^a-z0-9\s-]/g, '')
          .replace(/\s+/g, '-');
      }
      this.api.crearExamen(this.form).subscribe(() => { this.cargarTodo(); this.cerrarModal(); });
    }
  }

  editar() {
    if (this.seccionActiva === 'usuarios') {
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!this.form.email || !emailRegex.test(this.form.email)) {
        alert('Por favor, ingresa un formato de correo electrónico válido.');
        return;
      }
      this.form.username = this.form.email;
      
      this.api.editarUsuario(this.itemEditando.id, this.form).subscribe(() => { this.cargarTodo(); this.cerrarModal(); });
    } else if (this.seccionActiva === 'examenes') {
      this.api.editarExamen(this.itemEditando.slug, this.form).subscribe(() => { this.cargarTodo(); this.cerrarModal(); });
    }
  }

  eliminar(item: any) {
    if (!confirm('¿Eliminar este registro?')) return;

    if (this.seccionActiva === 'usuarios') {
      this.api.eliminarUsuario(item.id).subscribe(() => this.cargarTodo());
    } else if (this.seccionActiva === 'examenes') {
      this.api.eliminarExamen(item.slug).subscribe(() => this.cargarTodo());
    }
  }
}