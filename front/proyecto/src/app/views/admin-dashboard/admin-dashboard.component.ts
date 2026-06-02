import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../service/admin.service';

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

  constructor(private api: AdminService) {}

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
      this.api.crearUsuario(this.form).subscribe(() => { this.cargarTodo(); this.cerrarModal(); });
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