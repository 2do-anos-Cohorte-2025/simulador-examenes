import { CategoriaService } from '../../service/categoria.service';
import { NivelService } from '../../service/nivel.service';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-exam-form',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule, HttpClientModule],
  templateUrl: './exam-form.component.html',
  styleUrl: './exam-form.component.css'
})
export class ExamFormComponent {

  categorias: any[] = [];
  niveles: any[] = [];
  mensaje: string = "";
  examenForm: FormGroup;
  imagenSeleccionada: File | null = null;

  private apiUrl = 'http://127.0.0.1:8000/api/examenes/';


constructor(private fb: FormBuilder,private http : HttpClient,private categoriaService: CategoriaService,private nivelService: NivelService) {

  this.examenForm = this.fb.group({

    titulo: ['', [
      Validators.required,
      Validators.minLength(3),
      Validators.maxLength(50)
    ]],

    descripcion: ['', [
      Validators.required,
      Validators.minLength(10),
      Validators.maxLength(200)
    ]],

    categoria: [null],

    nivel: [null],

    tiempo_limite: ['', [
      Validators.required,
      Validators.min(1)
    ]]


  });

  this.cargarCategorias();
  this.cargarNiveles();

}

cargarCategorias() {
  this.categoriaService.getCategorias().subscribe({
    next: (data) => this.categorias = data,
    error: (err) => console.error('Error cargando categorías', err)
  });
}

cargarNiveles() {
  this.nivelService.getNiveles().subscribe({
    next: (data) => this.niveles = data,
    error: (err) => console.error('Error cargando niveles', err)
  });
}

crearSlug(titulo: string): string {
  return titulo
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-');
}

seleccionarImagen(event: Event) {
  const input = event.target as HTMLInputElement;

  if (input.files && input.files.length > 0) {
    this.imagenSeleccionada = input.files[0];
  }
}
  
crearExamen() {
    console.log("BOTON FUNCIONA");

    if (this.examenForm.invalid) {
      this.examenForm.markAllAsTouched();
      this.mensaje = 'Complete correctamente los campos';
      return;
    }

    const titulo = this.examenForm.get('titulo')?.value;
    const slug = this.crearSlug(titulo);
    
    const formData = new FormData();
    const token = localStorage.getItem('access_token');

    const headers = new HttpHeaders({
     Authorization: `Bearer ${token}`
    });

    formData.append('titulo', titulo);
    formData.append('slug', slug);
    formData.append('descripcion', this.examenForm.get('descripcion')?.value);
    formData.append('categoria', this.examenForm.get('categoria')?.value);
    formData.append('nivel', this.examenForm.get('nivel')?.value);
    formData.append('tiempo_limite', this.examenForm.get('tiempo_limite')?.value);

    if (this.imagenSeleccionada) {
      formData.append('imagen_examen', this.imagenSeleccionada);
    }

    this.http.post(this.apiUrl, formData, { headers }).subscribe({
      next: () => {
        this.mensaje = 'Examen creado correctamente';
        this.examenForm.reset();
        this.imagenSeleccionada = null;
      },
      error: (error) => {
        console.error(error);
        this.mensaje = 'Error al crear el examen';
      }
    });
  }
}




