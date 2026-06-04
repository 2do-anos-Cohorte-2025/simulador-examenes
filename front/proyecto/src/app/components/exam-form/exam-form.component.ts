import { CategoriaService } from '../../service/categoria.service';
import { NivelService } from '../../service/nivel.service';
import { ExamenService } from '../../service/examen.service';
import { PreguntaService } from '../../service/pregunta.service';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { HttpClient, HttpClientModule, HttpHeaders } from '@angular/common/http';

import { RouterLink } from '@angular/router';


@Component({
  selector: 'app-exam-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule, RouterLink],
  templateUrl: './exam-form.component.html',
  styleUrl: './exam-form.component.css'
})
export class ExamFormComponent {

  categorias: any[] = [];
  niveles: any[] = [];
  mensaje: string = "";
  examenForm: FormGroup;
  preguntaForm: FormGroup;
  opcionForm: FormGroup;
  imagenSeleccionada: File | null = null;
  imagenPreguntaSeleccionada: File | null = null;
  imagenOpcionSeleccionada: File | null = null;
  examenCreado: any = null;

  preguntaActual: any = null;

  preguntas: any[] = [];

  mostrarPreguntas = false;
  mostrarOpciones = false;


  private apiUrl = 'http://127.0.0.1:8000/api/examenes/';


  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private categoriaService: CategoriaService,
    private nivelService: NivelService,
    private examenService: ExamenService,
    private preguntaService: PreguntaService,
  ) {

    this.examenForm = this.fb.group({
      titulo: ['', [Validators.required]],
      descripcion: ['', [Validators.required]],
      categoria: [null],
      nivel: [null],
      tiempo_limite: ['', [Validators.required]]
    });

    this.categoriaService.getCategorias().subscribe({
      next: data => {
        this.categorias = data;
      },
      error: err => {
        console.log("Error categorias:", err);
      }
    });

    this.nivelService.getNiveles().subscribe({
      next: data => {
        console.log('Niveles:', data);
        this.niveles = data;
      }
    });

    this.preguntaForm = this.fb.group({
      enunciado: ['', Validators.required],
      puntos: [
        1.00,
        Validators.required
      ],
      tipo: ['opcion_multiple']
    });

    this.opcionForm = this.fb.group({
      texto_opcion: ['', Validators.required],
      es_correcta: [false]
    });

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

  seleccionarImagenPregunta(event: Event) {

    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      this.imagenPreguntaSeleccionada = input.files[0];
    }

  }
  seleccionarImagenOpcion(event: Event) {

    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      this.imagenOpcionSeleccionada = input.files[0];
    }

  }

  crearExamen() {

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
      next: (examen) => {

        this.examenCreado = examen;

        this.mostrarPreguntas = true;

        this.mensaje = 'Examen creado correctamente';

      },
      error: (error) => {
        console.error(error);
        this.mensaje = 'Error al crear el examen';
      }
    });
  }

  crearPregunta() {

    if (!this.examenCreado) return;

    const formData = new FormData();

    formData.append(
      'enunciado',
      this.preguntaForm.get('enunciado')?.value
    );

    formData.append(
      'tipo',
      this.preguntaForm.get('tipo')?.value
    );

    formData.append(
      'puntos',
      this.preguntaForm.get('puntos')?.value
    );

    formData.append(
      'examen',
      this.examenCreado.id.toString()
    );

    if (this.imagenPreguntaSeleccionada) {

      formData.append(
        'imagen_pregunta',
        this.imagenPreguntaSeleccionada
      );

    }

    this.preguntaService.createPregunta(formData)
      .subscribe({
        next: (pregunta) => {

          this.preguntaActual = pregunta;

          this.preguntas.push(pregunta);

          this.mostrarOpciones = true;

        }
      });

  }

  crearOpcion() {

    if (!this.preguntaActual) return;

    const formData = new FormData();

    formData.append(
      'pregunta',
      this.preguntaActual.id.toString()
    );

    formData.append(
      'texto_opcion',
      this.opcionForm.get('texto_opcion')?.value
    );

    formData.append(
      'es_correcta',
      this.opcionForm.get('es_correcta')?.value
    );

    if (this.imagenOpcionSeleccionada) {

      formData.append(
        'imagen_opcion',
        this.imagenOpcionSeleccionada
      );

    }

    this.preguntaService.createOpcion(formData)
      .subscribe({
        next: () => {

          this.opcionForm.reset({
            es_correcta: false
          });

          this.imagenOpcionSeleccionada = null;

        }
      });

  }

  nuevaPregunta() {

    this.preguntaActual = null;

    this.mostrarOpciones = false;

  }
}




