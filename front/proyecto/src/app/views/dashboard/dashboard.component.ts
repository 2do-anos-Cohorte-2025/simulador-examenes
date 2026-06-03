import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ExamFormComponent } from '../../components/exam-form/exam-form.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule,HttpClientModule,ExamFormComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {


  mostrarFormulario = false;
  mostrarExamenes = false;
  mostrarResultados = false;

  examenes: any[] = [];
  cargandoExamenes = false;
  errorExamenes = '';

  constructor(private http: HttpClient) {}

  mostrarCrearExamen() {
    this.mostrarFormulario = true;
    this.mostrarExamenes = false;
    this.mostrarResultados = false;
  }

  mostrarListaExamenes() {

  this.mostrarFormulario = false;
  this.mostrarExamenes = true;
  this.mostrarResultados = false;

  this.cargarExamenes();
  }

  mostrarResultadosExamenes() {

  this.mostrarFormulario = false;
  this.mostrarExamenes = false;
  this.mostrarResultados = true;
  }

  cargarExamenes() {
    this.cargandoExamenes = true;
    this.errorExamenes = '';

    this.http.get<any[]>('http://127.0.0.1:8000/api/examenes/').subscribe({
      next: (data) => {
        this.examenes = data;
        this.cargandoExamenes = false;
      },
      error: () => {
        this.errorExamenes = 'No se pudieron cargar los exámenes.';
        this.cargandoExamenes = false;
      }
    });
  }

}
