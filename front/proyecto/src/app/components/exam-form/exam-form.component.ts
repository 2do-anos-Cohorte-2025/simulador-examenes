import { Component } from '@angular/core';

@Component({
  selector: 'app-exam-form',
  standalone: true,
  imports: [],
  templateUrl: './exam-form.component.html',
  styleUrl: './exam-form.component.css'
})
export class ExamFormComponent {

  mensaje: string = "";

  crearExamen() {
    this.mensaje = "Examen creado correctamente";
  }

}
