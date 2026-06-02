import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { ExamFormComponent } from '../../components/exam-form/exam-form.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule,ExamFormComponent],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent {


  mostrarFormulario = false;
  mostrarExamenes = false;
  mostrarResultados = false;

  mostrarCrearExamen() {
    this.mostrarFormulario = true;
    this.mostrarExamenes = false;
    this.mostrarResultados = false;
  }

  mostrarListaExamenes() {

  this.mostrarFormulario = false;
  this.mostrarExamenes = true;
  this.mostrarResultados = false;
  }

  mostrarResultadosExamenes() {

  this.mostrarFormulario = false;
  this.mostrarExamenes = false;
  this.mostrarResultados = true;
  }


}
