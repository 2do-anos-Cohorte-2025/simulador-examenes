import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';

@Component({
  selector: 'app-exam-form',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule],
  templateUrl: './exam-form.component.html',
  styleUrl: './exam-form.component.css'
})
export class ExamFormComponent {

  mensaje: string = "";
  examenForm: FormGroup;

constructor(private fb: FormBuilder) {

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

    categoria: ['', Validators.required]

  });

}
  

  crearExamen() {
    if (this.examenForm.valid) {

    console.log(this.examenForm.value);

    this.mensaje = "Examen creado correctamente";

    this.examenForm.reset();

  } else {

    this.mensaje = "Complete correctamente los campos";

  }
 }

}
