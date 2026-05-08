import { Component } from '@angular/core';

@Component({
  selector: 'app-test-card',
  standalone: true,
  imports: [],
  templateUrl: './test-card.component.html',
  styleUrl: './test-card.component.css'
})
export class TestCardComponent {
  arrowUrl: string = 'assets/icons/arrow-up.svg';
  testsCardList: { id: number, titulo: string; imagen: string }[] = [
{ id:1, titulo: "Ciencia", imagen:"/assets/carousel/card-ciencias.png"},
{ id:2, titulo: "Educación", imagen:"/assets/carousel/card-educacion.png"},
{ id:3, titulo: "Escritura", imagen:"/assets/carousel/card-escritura.png"},
{ id:4, titulo: "Lenguaje", imagen:"/assets/carousel/card-lenguaje.png"},
{ id:5, titulo: "Matemática", imagen:"/assets/carousel/card-matematica.png"},
{ id:6, titulo: "Primario", imagen:"/assets/carousel/card-primario.png"},
{ id:7, titulo: "Quizzes", imagen:"/assets/carousel/card-quizz.png"},
{ id:8, titulo: "Ciencias Sociales", imagen:"/assets/carousel/card-sociales.png"},
]; 
}
